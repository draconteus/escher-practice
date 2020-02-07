const Koa = require('koa');
const Router = require('koa-router');
const bodyParser = require('koa-bodyparser');
const escherAuth = require('koa-escher-auth');
const EscherClient = require('escher-suiteapi-js');

const app = new Koa();
const router = new Router();

const escherMiddleware = escherAuth.authenticator({
  credentialScope: process.env.ESCHER_CREDENTIAL_SCOPE,
  keyPool: process.env.ESCHER_KEYPOOL
});

const createPythonClient = () => {
  const escherKey = process.env.PYTHON_ESCHER_KEY_ID;
  const escherSecret = process.env.PYTHON_ESCHER_SECRET
  const options = new EscherClient.Options(process.env.PYTHON_HOST, {
    secure: false,
    port: process.env.PYTHON_PORT,
    credentialScope: process.env.PYTHON_ESCHER_CREDENTIAL_SCOPE,
  })
  return EscherClient.create(escherKey, escherSecret, options)
}

app.use(bodyParser());

router.get('/', ctx => {
  ctx.body = "Ok, that's fine!";
});

router.get('/start', async ctx => {
  console.log('\nStart the ping-pong\n');
  const response = await createPythonClient().get('/ping');
  console.log('\nResponse from python service:' + response.body);
  ctx.body = response.body;
  ctx.status = response.statusCode;
})

router.get('/ping',
  escherMiddleware,
  async ctx => {
    ctx.body = '\nPong\n'
  }
)

app
  .use(router.routes())
  .use(router.allowedMethods());

app.listen(3000);

