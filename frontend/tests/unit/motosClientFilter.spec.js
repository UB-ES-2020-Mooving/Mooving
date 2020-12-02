import { shallowMount } from '@vue/test-utils'
import MotosClient from '@/components/MotosClient'
import flushPromises from 'flush-promises'

const $route = {
  query: { email: 'juanita@gmail.com' }
}
// fake api call:
jest.mock('axios', () => ({
  get: () => Promise.resolve(
    {
      data: {
        motos: [{
          id: 1,
          matricula: '1111-MMM',
          model_generic: 'basic',
          km_restantes: 80,
          address: 'Al Kufrah, Libia',
          last_coordinate_latitude: 23.4433,
          last_coordinate_longitude: 23.4432,
          distance: 13
        }]
      }
    })
}))

// eslint-disable-next-line no-undef
describe('Motos Page for Client', () => {
  // eslint-disable-next-line no-undef
  describe('when loaded', () => {
    // eslint-disable-next-line no-undef
    it('has the required two checkboxes', () => {
      const wrapper = shallowMount(MotosClient, {
        mocks: {
          $route
        }
      })
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#checkboxBasic').exists()).toBe(true)
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#checkboxPremium').exists()).toBe(true)
    })
    it('has the required slider', () => {
      const wrapper = shallowMount(MotosClient, {
        mocks: {
          $route
        }
      })
      // eslint-disable-next-line no-undef
      expect(wrapper.find('#sliderKmRestantes').exists()).toBe(true)
    })
  })
  describe('when a checkbox is clicked', () => {
    // eslint-disable-next-line no-undef
    it('the checkbox value and endpoints parameters change correctly', async () => {
      const wrapper = shallowMount(MotosClient, {
        mocks: {
          $route
        }
      })
      await flushPromises()
      await wrapper.setData(({ basic: true, premium: true }))
      expect(wrapper.vm.model_generic).toBe('all')
      await wrapper.find('#checkboxBasic').trigger('click')
      await flushPromises()
      expect(wrapper.vm.basic).toBe(false)
      expect(wrapper.vm.premium).toBe(true)
      expect(wrapper.vm.model_generic).toBe('premium')
    })
  })
  describe('when the slider value changed', () => {
    // eslint-disable-next-line no-undef
    it('if the slider value changed then endpoints parameters also change correctly', async () => {
      const wrapper = shallowMount(MotosClient, {
        mocks: {
          $route
        }
      })
      await flushPromises()
      wrapper.setData(({ more_km_restantes: 5 }))
      wrapper.setData(({ slider_km_restantes: '30' }))
      wrapper.vm.filterMotoListByKmRestantes()
      await flushPromises()
      expect(wrapper.vm.more_km_restantes).toBe(30)
    })
  })
})

