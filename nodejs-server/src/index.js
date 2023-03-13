import Koa from 'koa'
import cors from '@koa/cors'
import config from './config.js'
import dotenv from 'dotenv'

import { logger } from './middleware/logger.js'
import { router } from './router.js'

dotenv.config()

const app = new Koa()

// Let's log each successful interaction. We'll also log each error - but not here,
// that's be done in the json error-handling middleware
app.use(async (ctx, next) => {
  try {
    await next()
    logger.info(`${ctx.method} ${ctx.url} RESPONSE: ${ctx.response.status}`)
  } catch (err) {
    if (err?.kind === 'ObjectId') {
      err.status = 404
    } else {
      ctx.status = err.status || 500
      ctx.set('x-error-message', err.message)
      ctx.body = `服务器未知异常  x-error-message: ${err.message}`
    }
    logger.error(`${ctx.method} ${ctx.url} RESPONSE: ${ctx.response.status}  x-error-message: ${err.message}`)
  }
})

// return response time in X-Response-Time header
app.use(async function responseTime(ctx, next) {
  const t1 = Date.now()
  await next()
  const t2 = Date.now()
  ctx.set('X-Response-Time', `${Math.ceil(t2 - t1)}ms`)
  logger.info(`X-Response-Time ${Math.ceil(t2 - t1)}ms \n`)
})

app.use(cors({ origin: '*' }))

app.use(router.routes()).use(router.allowedMethods())

app.listen(3000)
logger.info(`listen at port 3000.`)