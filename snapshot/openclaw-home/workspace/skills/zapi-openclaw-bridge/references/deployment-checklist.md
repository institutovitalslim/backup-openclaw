# Deployment Checklist

## Transport
- webhook route tokenized
- HTTPS active
- nginx proxy working
- health endpoint reachable
- firewall rules correct

## Service
- systemd service enabled
- env file path correct
- bridge starts cleanly
- restart works cleanly
- logs are readable

## Logic
- patient/customer filter tested
- activation phrase tested
- new-contact behavior tested
- known-lead behavior tested
- pause tested
- resume tested
- assume tested
- release tested

## End-to-end
- inbound WhatsApp reaches bridge
- bridge calls concierge
- reply returns to WhatsApp
- blocked contact gets no reply
- allowed contact gets reply
