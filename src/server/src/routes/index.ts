import { FastifyInstance } from "fastify";
import healthRoutes from "./health/health.routes.js";

export default async function routes(app: FastifyInstance) {
  await app.register(healthRoutes, { prefix: '/health' });
}

