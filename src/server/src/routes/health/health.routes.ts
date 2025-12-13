import { FastifyInstance } from 'fastify'
import { askAi } from '../../services/ai.js'
import { responseSchema } from '../../schemas/index.js'

const healthSchema = (summary = 'Health Check') => ({
  tags: ['health'],
  summary,
  response: {
    ...responseSchema(),
  },
})

export default async function healthRoutes(app: FastifyInstance) {
  app.get('/ping', { schema: healthSchema() }, async () => {
    return {
      success: true,
      message: 'pong',
    }
  })

  app.get(
    '/ai',
    { schema: healthSchema('Check health of the AI sdk') },
    async (_req, reply) => {
      const result = await askAi()
      if (!result.success) {
        return reply.code(400).send(result)
      }
      return result
    }
  )
}
