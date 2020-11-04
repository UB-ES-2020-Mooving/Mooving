import { shallowMount } from '@vue/test-utils'
import Login from '@/components/Registration'

// eslint-disable-next-line no-undef
describe('Registration Page', () => {
  // eslint-disable-next-line no-undef
  describe('when loaded', () => {
    // eslint-disable-next-line no-undef
    it('has the required elements', () => {
      const wrapper = shallowMount(Login)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('button').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('button').text()).toBe('Register')
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#completeName').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#dniNie').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#iban').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#email').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#password').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#confirmPassword').exists()).toBe(true)
    })
  })
})
