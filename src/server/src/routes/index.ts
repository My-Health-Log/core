import fastifyPlugin from "fastify-plugin";
import { FastifyInstance } from "fastify";
import healthRoutes from "./health/health.routes.js";

async function routes(app: FastifyInstance) {
  await app.register(healthRoutes, { prefix: '/health' });
}

export default fastifyPlugin(routes);
