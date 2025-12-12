import Fastify, { FastifyInstance, RouteShorthandOptions } from 'fastify'
import swagger from './plugins/swagger.js'

const opts: RouteShorthandOptions = {
  schema: {
    response: {
      200: {
        type: 'object',
        properties: {
          pong: {
            type: 'string'
          }
        }
      }
    }
  }
}

export async function initApp() {

  const app: FastifyInstance = Fastify({ logger: true })
  await app.register(swagger);

  app.get('/ping', opts, async () => {
    return { pong: 'it worked!' }
  });

  return app;
}

