import fastifySwagger from "@fastify/swagger";
import fastifySwaggerUi from "@fastify/swagger-ui";
import { FastifyInstance } from "fastify";
import pkg from '../../package.json' with {type: 'json'}

export default function swagger(app: FastifyInstance) {
  app.register(fastifySwagger, {
    openapi: {
      openapi: '3.0.0',
      info: {
        title: 'My Health Logs API',
        description: pkg.version,
        version: pkg.version
      },
      servers: [
        {
          url: 'http://localhost:3000',
          description: 'Development server'
        }
      ],
      tags: [
        { name: 'user', description: 'User related end-points' },
        { name: 'code', description: 'Code related end-points' }
      ],
      externalDocs: {
        url: 'https://swagger.io',
        description: 'Find more info here'
      }
    }
  });

  app.register(fastifySwaggerUi, {
    routePrefix: "/docs"
  });
}
