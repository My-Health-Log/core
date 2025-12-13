import { google } from "@ai-sdk/google";
import { GoogleGenerativeAIModelId } from "@ai-sdk/google/internal";
import { generateObject } from "ai";
import { responseSchema } from "../schemas";

const HEALTH_CHECK_PROMPT =
  "You are a helpful assistant to help with health test of an API. If everything is working fine, respond with `API is healthy and responsive`";
const DEFAULT_MODEL_ID: GoogleGenerativeAIModelId = "gemini-2.5-flash-lite";

export async function askAi(
  prompt = HEALTH_CHECK_PROMPT,
  modelName = DEFAULT_MODEL_ID,
  schema = responseSchema()["200"],
) {
  const model = google(modelName);

  try {
    const output = await generateObject({ model, prompt, schema });
    return output.object;
  } catch (error) {
    return {
      success: false,
      message: "Error occured while trying to fetch response",
      error: {
        message: error instanceof Error ? error.message : String(error),
      },
    };
  }
}
