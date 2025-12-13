import z from "zod";

const envSchema = z.object({
  NODE_ENV: z
    .enum(["development", "production", "staging", "test"])
    .default("development"),
  PORT: z.string().default("3000").transform(Number),
  HOST: z.string().default("http://localhost"),
  // TODO: update this to min length 1 when db is added
  DB_URL: z.string().default(""),
  GOOGLE_GENERATIVE_AI_API_KEY: z.string().min(1, "Gemini API key is required"),
});

const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error("Failed to parse env: ", parsed.error);
  process.exit(1);
}

export const config = {
  env: parsed.data.NODE_ENV,
  server: {
    port: parsed.data.PORT,
    host: parsed.data.HOST,
  },
  db: {
    url: parsed.data.DB_URL,
  },
};
