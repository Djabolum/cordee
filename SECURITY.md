# Politique de sécurité

## Périmètre

Ce dépôt conserve un **prototype historique de serveur RAG**, pas une application de production complète. Sa publication sous licence libre ne signifie pas que ses endpoints sont prêts à être exposés à Internet ou que des correctifs sont garantis dans un délai défini.

Les routes `/upsert` et `/query` n'intègrent pas d'authentification. Le serveur écoute par défaut sur `127.0.0.1` ; ne pas modifier ce périmètre sans protections adaptées.

## Signaler une vulnérabilité

Merci de **ne pas divulguer de secrets, d'exploits ni de données personnelles dans une issue publique**.

- Si le bouton de signalement privé de GitHub est disponible dans l'onglet **Security** de ce dépôt, utilisez-le.
- Sinon, contactez le mainteneur par un canal privé indiqué sur son [profil GitHub](https://github.com/Djabolum) pour convenir d'un canal de transmission sécurisé.

L'absence de canal privé affiché ne constitue pas une autorisation de publier les détails d'une vulnérabilité.
