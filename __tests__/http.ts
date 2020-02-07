import { Matchers, Pact, Verifier } from '@pact-foundation/pact'
import fetch from 'node-fetch'
import * as path from 'path'
import * as rimraf from 'rimraf'
import * as util from 'util'

const rm = util.promisify(rimraf)

jest.setTimeout(30 * 1000)

const root = path.join(__dirname, '..')
const pactDir = path.join(root, 'pacts')

const httpPact = new Pact({
  consumer: 'notifications:http',
  provider: 'serlo.org:http',
  host: '0.0.0.0',
  port: 9009,
  log: path.join(root, 'pact-http.log'),
  dir: path.join(pactDir, 'http'),
  cors: true
})

beforeAll(async () => {
  await rm(pactDir)
  await httpPact.setup()
})

afterAll(async () => {
  await httpPact.finalize()
})

test('HTTP Contract', async () => {
  await httpPact.addInteraction({
    state: 'a event with id 234 exists',
    uponReceiving: 'render event 234 in format html',
    withRequest: {
      method: 'POST',
      path: '/events/render/html',
      body: ['234']
    },
    willRespondWith: {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: {
        '234': {
          content: Matchers.string()
        }
      }
    }
  })
  await new Verifier({
    provider: 'notifications:http',
    providerBaseUrl: 'http://localhost:8000',
    pactBrokerUrl: 'https://pacts.serlo.org',
    validateSSL: false,
    stateHandlers: {
      'no notifications exist': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'no notifications exist'
          })
        })
      },
      'a notification for user 123 and event 234 exists': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'a notification for user 123 and event 234 exists'
          })
        })
      }
    }
  }).verifyProvider()
  await httpPact.verify()
})
