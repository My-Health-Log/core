import { initApp } from "./app.js"

const start = async () => {
  const app = await initApp();
  try {
    await app.listen({ port: 3000 })
  } catch (err) {
    app.log.error(err)
    process.exit(1)
  }
}

start()
