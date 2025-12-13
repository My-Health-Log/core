import { FastifyInstance } from "fastify";
import { z } from "zod";
import { askAi } from "../../services/ai.js";

const healthSchema = {
  tags: ["health"],
  summary: "Health check",
  response: {
    200: z.object({ pong: z.string() }),
  },
};
const aiHealthSchema = {
  ...healthSchema,
  summary: "Check health of the AI sdk",
};

export default async function healthRoutes(app: FastifyInstance) {
  app.get("/ping", { schema: healthSchema }, async () => {
    return { pong: "it worked!" };
  });

  app.get("/ai", { schema: aiHealthSchema }, async () => {
    return await askAi();
  });
}
