import { MessageProviderPact } from '@pact-foundation/pact'
import fetch from 'node-fetch'

jest.setTimeout(30 * 1000)

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
        await fetch('http://localhost:8000/pact/execute-message/', {
          method: 'POST',
          body: JSON.stringify(message)
        })
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
        await fetch('http://localhost:8000/pact/execute-message/', {
          method: 'POST',
          body: JSON.stringify(message)
        })
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
        await fetch('http://localhost:8000/pact/execute-message/', {
          method: 'POST',
          body: JSON.stringify(message)
        })
        return message
      }
    },
    consumer: 'serlo.org:messages',
    provider: 'notifications:messages',
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
      'one event with id 123 exists': () => {
        return fetch('http://localhost:8000/pact/set-state/', {
          method: 'POST',
          body: JSON.stringify({
            consumer: 'serlo.org',
            state: 'one event with id 123 exists'
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
    },
    pactBrokerUrl: 'https://pacts.serlo.org'
  }).verify()
})
