import Fastify, { FastifyInstance, RouteShorthandOptions } from 'fastify'
import swagger from './plugins/swagger.js'

const server: FastifyInstance = Fastify({ logger: true })
await server.register(swagger);

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

server.get('/ping', opts, async () => {
  return { pong: 'it worked!' }
})

const start = async () => {
  try {
    await server.listen({ port: 3000 })
  } catch (err) {
    server.log.error(err)
    process.exit(1)
  }
}

start()
