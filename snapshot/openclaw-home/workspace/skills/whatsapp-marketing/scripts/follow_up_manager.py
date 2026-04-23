#!/usr/bin/env python3
"""
Sistema de Follow-up Automatizado para WhatsApp
Instituto Vital Slim

Gerencia sequências de mensagens para leads que não agendaram consulta.
"""

import json
import os
import time
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import requests

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/follow_up.log')
    ]
)
logger = logging.getLogger(__name__)


class FollowUpManager:
    """Gerenciador de follow-up automatizado via Z-API."""
    
    def __init__(self, config_path: str, leads_path: str):
        self.config = self._load_config(config_path)
        self.leads = self._load_leads(leads_path)
        self.zapi_base = os.getenv('ZAPI_BASE_URL', '').rstrip('/')
        self.zapi_token = os.getenv('ZAPI_TOKEN', '')
        self.zapi_client_token = os.getenv('ZAPI_CLIENT_TOKEN', '')
        
        if not self.zapi_base:
            raise ValueError("ZAPI_BASE_URL não configurado")
    
    def _load_config(self, path: str) -> dict:
        """Carrega configuração de mensagens."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_leads(self, path: str) -> List[Dict]:
        """Carrega lista de leads."""
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_leads(self, path: str):
        """Salva estado atualizado dos leads."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.leads, f, indent=2, ensure_ascii=False)
    
    def _is_business_hours(self) -> bool:
        """Verifica se está dentro do horário comercial (BRT)."""
        now = datetime.now()
        start = self.config['business_hours']['start']
        end = self.config['business_hours']['end']
        return start <= now.hour < end
    
    def _send_message(self, phone: str, text: str) -> bool:
        """Envia mensagem via Z-API."""
        if not self._is_business_hours():
            logger.info(f"Fora do horário comercial. Mensagem agendada para {phone}")
            return False
        
        url = f"{self.zapi_base}/send-text"
        
        # Remove caracteres não numéricos do telefone
        phone_clean = ''.join(filter(str.isdigit, phone))
        if not phone_clean.startswith('55'):
            phone_clean = '55' + phone_clean
        
        payload = {
            "phone": phone_clean,
            "message": text
        }
        
        headers = {
            "Content-Type": "application/json",
            "Client-Token": self.zapi_client_token
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get('messageSent'):
                    logger.info(f"Mensagem enviada para {phone}")
                    return True
                else:
                    logger.warning(f"Falha ao enviar para {phone}: {result}")
                    return False
            else:
                logger.error(f"Erro HTTP {response.status_code} para {phone}")
                return False
        except Exception as e:
            logger.error(f"Exceção ao enviar para {phone}: {e}")
            return False
    
    def _should_send(self, lead: Dict, message: Dict) -> bool:
        """Verifica se a mensagem deve ser enviada."""
        # Se já agendou, não envia
        if lead.get('scheduled', False):
            return False
        
        # Se já respondeu, não envia mais follow-up
        if lead.get('responded', False):
            return False
        
        # Se já enviou esta mensagem, não envia novamente
        sent_messages = lead.get('sent_messages', [])
        if message['id'] in sent_messages:
            return False
        
        # Verifica se passou o tempo desde a última interação
        last_contact = lead.get('last_contact')
        if not last_contact:
            return False
        
        last_contact_dt = datetime.fromisoformat(last_contact)
        delay = timedelta(hours=message['delay_hours'])
        now = datetime.now()
        
        # Verifica se está no horário correto
        if now < last_contact_dt + delay:
            return False
        
        # Verifica se já passou do horário máximo (não enviar mensagem muito tarde)
        max_delay = delay + timedelta(hours=24)
        if now > last_contact_dt + max_delay:
            # Marca como expirado
            lead['expired'] = True
            return False
        
        return True
    
    def _personalize(self, text: str, lead: Dict) -> str:
        """Personaliza mensagem com dados do lead."""
        nome = lead.get('nome', 'amiga')
        # Capitaliza primeira letra
        nome = nome.strip().title() if nome else 'amiga'
        
        return text.replace('{nome}', nome)
    
    def process_leads(self):
        """Processa todos os leads e envia mensagens quando apropriado."""
        sequence = self.config['sequences']['lead_no_schedule']
        messages = sequence['messages']
        
        sent_count = 0
        skipped_count = 0
        
        for lead in self.leads:
            phone = lead.get('phone', lead.get('whatsapp', ''))
            if not phone:
                logger.warning(f"Lead sem telefone: {lead.get('nome', 'desconhecido')}")
                skipped_count += 1
                continue
            
            # Tenta enviar cada mensagem da sequência
            for message in messages:
                if not self._should_send(lead, message):
                    continue
                
                # Personaliza texto
                text = self._personalize(message['text'], lead)
                
                # Envia mensagem
                if self._send_message(phone, text):
                    # Atualiza lead
                    if 'sent_messages' not in lead:
                        lead['sent_messages'] = []
                    lead['sent_messages'].append(message['id'])
                    lead['last_message_sent'] = datetime.now().isoformat()
                    sent_count += 1
                else:
                    skipped_count += 1
        
        logger.info(f"Processamento concluído: {sent_count} enviadas, {skipped_count} puladas")
        return sent_count, skipped_count
    
    def add_lead(self, nome: str, phone: str, source: str = "manual"):
        """Adiciona novo lead ao sistema."""
        phone_clean = ''.join(filter(str.isdigit, phone))
        if not phone_clean.startswith('55'):
            phone_clean = '55' + phone_clean
        
        lead = {
            "nome": nome,
            "phone": phone_clean,
            "source": source,
            "created_at": datetime.now().isoformat(),
            "last_contact": datetime.now().isoformat(),
            "scheduled": False,
            "responded": False,
            "sent_messages": []
        }
        
        self.leads.append(lead)
        logger.info(f"Lead adicionado: {nome} ({phone_clean})")
        return lead
    
    def mark_scheduled(self, phone: str):
        """Marca lead como agendado."""
        for lead in self.leads:
            if lead.get('phone') == phone or lead.get('whatsapp') == phone:
                lead['scheduled'] = True
                logger.info(f"Lead marcado como agendado: {phone}")
                return True
        return False
    
    def mark_responded(self, phone: str):
        """Marca lead como respondido."""
        for lead in self.leads:
            if lead.get('phone') == phone or lead.get('whatsapp') == phone:
                lead['responded'] = True
                logger.info(f"Lead marcado como respondido: {phone}")
                return True
        return False
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do follow-up."""
        total = len(self.leads)
        scheduled = sum(1 for l in self.leads if l.get('scheduled'))
        responded = sum(1 for l in self.leads if l.get('responded'))
        expired = sum(1 for l in self.leads if l.get('expired'))
        active = total - scheduled - responded - expired
        
        return {
            "total_leads": total,
            "scheduled": scheduled,
            "responded": responded,
            "expired": expired,
            "active_in_followup": active,
            "conversion_rate": round(scheduled / total * 100, 2) if total > 0 else 0
        }


def main():
    parser = argparse.ArgumentParser(description='Follow-up WhatsApp - Instituto Vital Slim')
    parser.add_argument('--config', default='follow_up_config.json', help='Arquivo de configuração')
    parser.add_argument('--leads', default='leads.json', help='Arquivo de leads')
    parser.add_argument('--add', nargs=2, metavar=('NOME', 'TELEFONE'), help='Adicionar novo lead')
    parser.add_argument('--scheduled', metavar='TELEFONE', help='Marcar lead como agendado')
    parser.add_argument('--responded', metavar='TELEFONE', help='Marcar lead como respondido')
    parser.add_argument('--stats', action='store_true', help='Mostrar estatísticas')
    parser.add_argument('--run', action='store_true', help='Executar follow-up')
    
    args = parser.parse_args()
    
    manager = FollowUpManager(args.config, args.leads)
    
    if args.add:
        nome, phone = args.add
        manager.add_lead(nome, phone)
        manager._save_leads(args.leads)
        print(f"✅ Lead adicionado: {nome} ({phone})")
    
    elif args.scheduled:
        if manager.mark_scheduled(args.scheduled):
            manager._save_leads(args.leads)
            print(f"✅ Lead marcado como agendado: {args.scheduled}")
        else:
            print(f"❌ Lead não encontrado: {args.scheduled}")
    
    elif args.responded:
        if manager.mark_responded(args.responded):
            manager._save_leads(args.leads)
            print(f"✅ Lead marcado como respondido: {args.responded}")
        else:
            print(f"❌ Lead não encontrado: {args.responded}")
    
    elif args.stats:
        stats = manager.get_stats()
        print("\n📊 ESTATÍSTICAS DO FOLLOW-UP")
        print("=" * 40)
        print(f"Total de leads: {stats['total_leads']}")
        print(f"Agendados: {stats['scheduled']}")
        print(f"Responderam: {stats['responded']}")
        print(f"Expirados: {stats['expired']}")
        print(f"Ativos no follow-up: {stats['active_in_followup']}")
        print(f"Taxa de conversão: {stats['conversion_rate']}%")
    
    elif args.run:
        logger.info("Iniciando processamento de follow-up...")
        sent, skipped = manager.process_leads()
        manager._save_leads(args.leads)
        print(f"\n✅ Processamento concluído!")
        print(f"Mensagens enviadas: {sent}")
        print(f"Mensagens puladas: {skipped}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
