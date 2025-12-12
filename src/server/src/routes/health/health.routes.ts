import { FastifyInstance } from "fastify";
import { z } from 'zod'

const pingSchema = {
  tags: ['health'],
  summary: 'Health check',
  response: {
    200: z.object({ pong: z.string() })
  }
}

export default async function healthRoutes(app: FastifyInstance) {
  app.get('/ping', { schema: pingSchema }, async () => {
    return { pong: 'it worked!' }
  });
}
