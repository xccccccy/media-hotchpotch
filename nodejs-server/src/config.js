import dotenv from 'dotenv'

dotenv.config()

export default {
  http: {
    prefix: process.env.HTTP_PREFIX || ''
  },
  meting: {
    url: process.env.METING_URL || '',
    api: process.env.METING_API || process.env.METING_SERVER_ADDR || 'http://127.0.0.1:5002',
    token: process.env.METING_TOKEN || 'token'
  }
}
