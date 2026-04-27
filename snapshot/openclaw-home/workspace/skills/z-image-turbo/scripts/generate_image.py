#!/usr/bin/env python3
"""
Z-Image-Turbo Image Generator
Wrapper para o HuggingFace Space mrfakename/Z-Image-Turbo
Modelo: Fast SDXL/Flux inference (~9 steps, ~2-5s)
"""

import sys
import os
import argparse
from gradio_client import Client

def generate_image(prompt, output_path=None, height=1024, width=1024, steps=9, seed=None):
    """
    Gera imagem usando Z-Image-Turbo no HuggingFace Spaces.
    
    Args:
        prompt: Texto descrição da imagem (obrigatório)
        output_path: Caminho para salvar a imagem (opcional)
        height: Altura da imagem (padrão: 1024)
        width: Largura da imagem (padrão: 1024)
        steps: Número de inference steps (padrão: 9, mínimo: 1, máximo: 50)
        seed: Seed para reprodutibilidade (opcional, aleatório se não informado)
    
    Returns:
        dict com 'path', 'url', 'seed_used'
    """
    
    client = Client('mrfakename/Z-Image-Turbo')
    
    randomize_seed = seed is None
    if seed is None:
        seed = 42  # valor default, será randomizado pelo backend
    
    result = client.predict(
        prompt=prompt,
        height=float(height),
        width=float(width),
        num_inference_steps=float(steps),
        seed=int(seed),
        randomize_seed=randomize_seed,
        api_name='/generate_image'
    )
    
    image_path = result[0]
    seed_used = result[1]
    
    # Se output_path foi especificado, copiar para lá
    if output_path and os.path.exists(image_path):
        import shutil
        shutil.copy2(image_path, output_path)
        final_path = output_path
    else:
        final_path = image_path
    
    return {
        'path': final_path,
        'seed_used': seed_used,
        'prompt': prompt,
        'dimensions': f"{int(width)}x{int(height)}"
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Z-Image-Turbo Image Generator')
    parser.add_argument('--prompt', '-p', required=True, help='Text prompt for image generation')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--height', type=int, default=1024, help='Image height (default: 1024)')
    parser.add_argument('--width', type=int, default=1024, help='Image width (default: 1024)')
    parser.add_argument('--steps', type=int, default=9, help='Inference steps (default: 9)')
    parser.add_argument('--seed', type=int, help='Random seed (optional)')
    
    args = parser.parse_args()
    
    try:
        result = generate_image(
            prompt=args.prompt,
            output_path=args.output,
            height=args.height,
            width=args.width,
            steps=args.steps,
            seed=args.seed
        )
        print(f"✅ Imagem gerada com sucesso!")
        print(f"📁 Caminho: {result['path']}")
        print(f"🎲 Seed usada: {result['seed_used']}")
        print(f"📐 Dimensões: {result['dimensions']}")
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)
