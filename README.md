# Lives do Cellbit

O Lives do Cellbit é um bot que notifica:

- Quando uma live começar
- Quando o jogo for trocado
- Quando uma live se encerrar

## Como posso usar-lo?

Você pode seguir o bot no twitter ([@livesdocellbit](https://twitter.com/livesdocellbit "@livesdocellbit"))  e ativar as notificações caso queira :D

## Como faço para hospeda-lô? 

Em breve, farei um tutorial de como fazer isto.

## Backend de publicação Xquik

Por padrão, o bot usa Tweepy. Para enviar posts de texto pelo Xquik, configure:

```env
POST_BACKEND=xquik
XQUIK_API_KEY=
XQUIK_ACCOUNT=
XQUIK_BASE_URL=https://xquik.com
```

Posts com imagem local continuam usando Tweepy e as variáveis `TWITTER_*`, pois o Xquik recebe URLs de mídia públicas.

## Com posso te apoiar?

Você pode me apoiar dando uma estrela no projeto ou me seguindo em alguma rede social minha. Caso queira me apoiar financeiramente, acesse [minha página do Ko-fi](http://https://ko-fi.com/admvicli "minha página do Ko-fi"), qualquer valor é bem vindo!

### Licença:

Projeto licenciado nos termos da Licença MIT.
