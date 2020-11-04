import { shallowMount } from '@vue/test-utils'
import Login from '@/components/Login'

// eslint-disable-next-line no-undef
describe('Login Page', () => {
  // eslint-disable-next-line no-undef
  describe('when loaded', () => {
    // eslint-disable-next-line no-undef
    it('has the required elements', () => {
      const wrapper = shallowMount(Login)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('button').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('button').text()).toBe('Log in')
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#email').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#password').exists()).toBe(true)
    })
  })
  // eslint-disable-next-line no-undef
  describe('User login inputs ', () => {
    // eslint-disable-next-line no-undef
    it('has the correct inputs', async () => {
      const wrapper = shallowMount(Login)
      const emailInput = wrapper.find('input[type="email"]')
      await emailInput.setValue('1234567@gmail.com')
      // eslint-disable-next-line no-undef
      expect(wrapper.find('input[type="email"]').element.value).toBe('1234567@gmail.com')
      const passwordInput = wrapper.find('input[type="password"]')
      await passwordInput.setValue('1234567')
      // eslint-disable-next-line no-undef
      expect(wrapper.find('input[type="password"]').element.value).toBe('1234567')
    })
  })
})
