import Router from 'koa-router'
import dayjs from 'dayjs'
import apiService from './service/music-api.js'
import config from './config.js'

export const router = new Router()

router.get(`${config.http.prefix}/api`, apiService)
router.get(`${config.http.prefix}/`, apiService)