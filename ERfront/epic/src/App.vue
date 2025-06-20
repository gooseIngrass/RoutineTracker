<template>
  <div class="app_container">
    <router-view />
    <widget-container-modal />
    <Navbar v-if="showNavBar" />
  </div>
</template>

<script>
  import Navbar from './components/Navbar.vue'
  import {container} from "jenesius-vue-modal"

  export default{
    name: 'App',
    components:{
      Navbar,
      WidgetContainerModal: container
    },
    computed:{
      showNavBar(){
        return this.$route.path !== '/welcome'
      }
    }
  }
</script>

<style scoped>
.app_container {
  display: flex;
  flex-direction: column;
  min-height: 98vh;
}
</style>
