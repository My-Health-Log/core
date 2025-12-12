import Fastify, { FastifyInstance } from 'fastify'
import swagger from './plugins/swagger.js'
import routes from './routes/index.js';
import { serializerCompiler, validatorCompiler, ZodTypeProvider } from 'fastify-type-provider-zod';

export async function initApp() {

  const app: FastifyInstance = Fastify({ logger: true }).withTypeProvider<ZodTypeProvider>();

  app.setValidatorCompiler(validatorCompiler);
  app.setSerializerCompiler(serializerCompiler);

  await app.register(routes);

  return app;
}

