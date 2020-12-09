import { shallowMount } from '@vue/test-utils'
import ConfirmDeleteAccountDialog from '@/components/ConfirmDeleteAccountDialog.vue'

const $route = {
    query: { email: 'juanita@gmail.com' }
  }

// eslint-disable-next-line no-undef
describe('Confirm Delete Account Dialog', () => {
  // eslint-disable-next-line no-undef
  describe('when loaded', () => {
    // eslint-disable-next-line no-undef
    it('has the required elements', () => {
      const wrapper = shallowMount(ConfirmDeleteAccountDialog, {
        mocks: {
          $route
        }
      })
      // eslint-disable-next-line no-undef
      expect(wrapper.find('button').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('button').text()).toBe('Confirm')
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#password').exists()).toBe(true)
    })
  })
  // eslint-disable-next-line no-undef
  describe('User confirm inputs ', () => {
    // eslint-disable-next-line no-undef
    it('has the correct inputs', async () => {
      const wrapper = shallowMount(ConfirmDeleteAccountDialog, {
        mocks: {
          $route
        }
      })
      const passwordInput = wrapper.find('input[type="password"]')
      await passwordInput.setValue('1234567')
      // eslint-disable-next-line no-undef
      expect(wrapper.find('input[type="password"]').element.value).toBe('1234567')
    })
  })
})
