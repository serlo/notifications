import { MessageProviderPact, Verifier } from '@pact-foundation/pact'

import axios from 'axios'
import * as path from 'path'

const root = path.join(__dirname, '..')

test('HTTP Contract', async () => {
  await new Verifier({
    provider: 'notifications:http',
    providerBaseUrl: 'http://localhost:8000',
    // TODO: Can't use pactBrokerUrl
    pactUrls: [
      'https://pacts.serlo.org/pacts/provider/notifications%3Ahttp/consumer/serlo.org%3Ahttp/latest'
    ],
    validateSSL: false,
    stateHandlers: {
      'no notifications exist': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'no notifications exist'
        })
      },
      'a notification for user 123 and event 234 exists': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'a notification for user 123 and event 234 exists'
        })
      }
    }
  }).verifyProvider()
})

test('Message Contract', async () => {
  await new MessageProviderPact({
    messageProviders: {
      'a `create-event` message': async () => {
        const message = {
          type: 'create-event',
          payload: {
            event: { provider_id: 'serlo.org', id: '123' },
            created_at: '2015-08-06T16:53:10+01:00',
            source: { provider_id: 'serlo.org' }
          }
        }

        await axios.post('http://localhost:8000/pact/execute-message/', message)
        return message
      },
      'a `create-notification` message': async () => {
        const message = {
          type: 'create-notification',
          payload: {
            event: { provider_id: 'serlo.org', id: '123' },
            user: { provider_id: 'serlo.org', id: '234' },
            source: { provider_id: 'serlo.org' }
          }
        }
        await axios.post('http://localhost:8000/pact/execute-message/', message)
        return message
      },
      'a `read-notification` message': async () => {
        const message = {
          type: 'read-notification',
          payload: {
            event: { provider_id: 'serlo.org', id: '234' },
            user: { provider_id: 'serlo.org', id: '123' },
            created_at: '2015-08-06T16:53:10+01:00',
            source: { provider_id: 'serlo.org' }
          }
        }
        await axios.post('http://localhost:8000/pact/execute-message/', message)
        return message
      }
    },
    consumer: 'serlo.org:messages',
    provider: 'notifications:messages',
    stateHandlers: {
      'no notifications exist': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'no notifications exist'
        })
      },
      'one event with id 123 exists': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'one event with id 123 exists'
        })
      },
      'a notification for user 123 and event 234 exists': () => {
        return axios.post('http://localhost:8000/pact/set-state/', {
          consumer: 'serlo.org',
          state: 'a notification for user 123 and event 234 exists'
        })
      }
    },
    // TODO: Can't use pactBrokerUrl
    pactUrls: [
      'https://pacts.serlo.org/pacts/provider/notifications%3Amessages/consumer/serlo.org%3Amessages/latest'
    ]
  }).verify()
})