import fastifyPlugin from "fastify-plugin";
import fastifySwagger from "@fastify/swagger";
import fastifySwaggerUi from "@fastify/swagger-ui";
import { FastifyInstance } from "fastify";
import pkg from '../../package.json' with {type: 'json'}
import { jsonSchemaTransform, jsonSchemaTransformObject } from "fastify-type-provider-zod";

async function swagger(app: FastifyInstance) {
  await app.register(fastifySwagger, {
    transform: jsonSchemaTransform,
    transformObject: jsonSchemaTransformObject,
    openapi: {
      openapi: '3.0.0',
      info: {
        title: 'My Health Logs API',
        description: pkg.description,
        version: pkg.version
      },
      servers: [
        {
          url: 'http://localhost:3000',
          description: 'Development server'
        }
      ],
      tags: [
        { name: 'health', description: 'Server health related end-points' },
        { name: 'report', description: 'Report generation related end-points' },
        { name: 'parse', description: 'Data parser related end-points' }
      ],
    },
  });

  await app.register(fastifySwaggerUi, {
    routePrefix: "/docs"
  });
}

export default fastifyPlugin(swagger);
