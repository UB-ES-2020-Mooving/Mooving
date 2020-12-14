import { shallowMount } from '@vue/test-utils'
import mechanicMoto from '@/components/MechanicMoto'
import ModifyMotoForm from '@/components/ModifyMotoForm.vue'
import flushPromises from 'flush-promises'

const $route = {
  query: { email: '1111111j@mooving.com', id: 1 }
}
const mockRouter = {
  push: jest.fn()
}

jest.mock('axios', () => ({
  get: () => Promise.resolve(
    {
      data: {
        mechanic_moto: {
          id: 1,
          matricula: '1111-MMM',
          state: 'AVAILABLE',
          time_since_last_check: 0,
          km_since_last_check: 0,
          km_total: 100,
          time_total: 10,
          type: 'basic',
          km_restantes: 80,
          address: 'Al Kufrah, Libia',
          last_coordinate_latitude: 23.4433,
          last_coordinate_longitude: 23.4432,
          distance: 13
        }
      }
    })
}))

describe('Motos Page for Mechanic', () => {
  // eslint-disable-next-line no-undef
  describe('when loaded', () => {
    // eslint-disable-next-line no-undef
    it('has the required modify button', () => {
      const wrapper = shallowMount(mechanicMoto, {
        mocks: {
          $route
        }
      })
      expect(wrapper.find('#modifyButton').exists()).toBe(true)
    })
  })
  describe('when a modify button is clicked', () => {
    // eslint-disable-next-line no-undef
    it('route to modify form', async () => {
      const wrapper = shallowMount(mechanicMoto, {
        mocks: {
          $route,
          $router: mockRouter
        }
      })
      await wrapper.setData(({ path: '/modifyMotoForm', query: { email: '1111111j@mooving.com', id: 1 } }))
      await wrapper.find('#modifyButton').trigger('click')
      expect(mockRouter.push).toHaveBeenCalledWith({ path: '/modifyMotoForm', query: { email: '1111111j@mooving.com', id: 1 } })
    })
  })
})

describe('Modify Moto Form for Mechanic', () => {
  // eslint-disable-next-line no-undef
  describe('when loaded', () => {
    // eslint-disable-next-line no-undef
    it('has the required elements', () => {
      const wrapper = shallowMount(ModifyMotoForm, {
        mocks: {
          $route
        }
      })
      expect(wrapper.find('#licensePlate').exists()).toBe(true)
      expect(wrapper.find('#battery').exists()).toBe(true)
      expect(wrapper.find('#state').exists()).toBe(true)
      expect(wrapper.find('#cancelButton').exists()).toBe(true)
      expect(wrapper.find('#cancelButton').text()).toBe('Cancel')
      expect(wrapper.find('#saveButton').exists()).toBe(true)
      expect(wrapper.find('#saveButton').text()).toBe('Save')
    })
  })
  describe('when cancel button is clicked', () => {
    // eslint-disable-next-line no-undef
    it('route to moto info Page for mechanic', async () => {
      const wrapper = shallowMount(ModifyMotoForm, {
        mocks: {
          $route,
          $router: mockRouter
        }
      })
      await wrapper.find('#cancelButton').trigger('click')
      expect(mockRouter.push).toHaveBeenCalledWith({ path: '/mechanicMoto', query: { email: '1111111j@mooving.com', id: 1 } })
    })
  })
})


