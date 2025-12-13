import { initApp } from './app.js'
import { config } from './config.js'

const start = async () => {
  const app = await initApp()
  try {
    await app.listen({ port: config.server.port })
    const host = config.server.host || 'localhost'
    const port = config.server.port
    app.log.info(`Server listening at http://${host}:${port}`)
    app.log.info(`API docs available at http://${host}:${port}/docs`)
  } catch (err) {
    app.log.error(err)
    process.exit(1)
  }
}

start()
