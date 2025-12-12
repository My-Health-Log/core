import { initApp } from "./app.js"
import { config } from "./config.js";

const start = async () => {
  const app = await initApp();
  try {
    await app.listen({ port: config.server.port })
  } catch (err) {
    app.log.error(err)
    process.exit(1)
  }
}

start()
