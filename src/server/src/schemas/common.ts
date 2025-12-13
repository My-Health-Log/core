import z from 'zod'

export const responseSchema = (dataSchema = {}) => ({
  200: z.object({
    success: z.boolean(),
    message: z.string(),
    data: z.object(dataSchema).optional(),
  }),
  400: z.object({
    success: z.boolean(),
    message: z.string(),
    error: z.object({ message: z.string() }).optional(),
  }),
})
