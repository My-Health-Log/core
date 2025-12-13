import { google } from "@ai-sdk/google";
import { GoogleGenerativeAIModelId } from "@ai-sdk/google/internal";
import { generateObject } from "ai";
import z from "zod";

const HEALTH_CHECK_PROMPT = `
You are a helpful assistant to help with health test of an API.
`;
const DEFAULT_MODEL_ID:GoogleGenerativeAIModelId = 'gemini-2.5-flash-lite';

const HEALTH_CHECK_SCHEMA =z.object({
    success: z.boolean(),
    message: z.string(),
    data: z.object().optional(),
    error: z.object().optional(),
  });

export async function askAi(prompt=HEALTH_CHECK_PROMPT,modelName = DEFAULT_MODEL_ID, schema=HEALTH_CHECK_SCHEMA){
  const model = google(modelName);

  const output = await generateObject({ model, prompt, schema});

  return output.toJsonResponse();
}
