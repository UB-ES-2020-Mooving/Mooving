// Import the `mount()` method from Vue Test Utils
import {createLocalVue, shallowMount} from '@vue/test-utils'
import Profile from '../../src/components/Profile'

const $route = {
  query: { email: 'juanita@gmail.com' }
}
jest.mock('axios', () => ({
  get: () => Promise.resolve()(
      {
        data: {
          client_profile: {
            nombre: 'Juana',
            iban: '2223462362665251w',
            dni_nie: '11111111J',
            email: 'juanita@gmail.com'
          }
        }
      }
  )
}))
// eslint-disable-next-line no-undef
describe('Profile Page', () => {
  // eslint-disable-next-line no-undef
  it('has the required elements', () => {
    const wrapper = shallowMount(Profile, {
      mocks: {
          $route
        }
    })
    wrapper.setData(({ email: "juanita@gmail.com" }))
    // eslint-disable-next-line no-undef
    expect(wrapper.findAll("h6").filter(node => node.text().match("Name")).exists()).toBe(true)
    // eslint-disable-next-line no-undef
    expect(wrapper.findAll("h6").filter(node => node.text().match("Email")).exists()).toBe(true)
    // eslint-disable-next-line no-undef
    expect(wrapper.findAll("h6").filter(node => node.text().match("IBAN")).exists()).toBe(true)
    // eslint-disable-next-line no-undef
    expect(wrapper.findAll("h6").filter(node => node.text().match("DNI/NIE")).exists()).toBe(true)
  })
})
describe('User gets their data ', () => {
  // eslint-disable-next-line no-undef
  it('has the correct output', async () => {
    const wrapper = shallowMount(Profile, {
      mocks: {
        $route
      }
    })
    await flushPromises()
    await wrapper.setData(({ email: "juanita@gmail.com" }))
    await flushPromises()
    expect(wrapper.nombre).toBe('Juana')
    expect(wrapper.iban).toBe('2223462362665251w')
    expect(wrapper.dni_nie).toBe('11111111J')
    expect(wrapper.email).toBe('juanita@gmail.com')
  })
})