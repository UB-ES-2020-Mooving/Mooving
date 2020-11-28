// Import the `mount()` method from Vue Test Utils
import {createLocalVue, shallowMount} from '@vue/test-utils'
import Profile from '../../src/components/Profile'
import VueRouter from 'vue-router'

const localVue = createLocalVue()
localVue.use(VueRouter)
const router = new VueRouter()
// eslint-disable-next-line no-undef
describe('Profile Page', () => {
  // eslint-disable-next-line no-undef
  it('only displays data ', () => {
    const wrapper = shallowMount(Profile, {
      router,
      localVue
    })
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
