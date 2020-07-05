<template>
  <div id="app">
    <UploadImg/>
  </div>
</template>

<script>
import UploadImg from './components/UploadImg.vue'

export default {
  name: 'App',
  components: {
    UploadImg
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 2 0px;
  padding-left: 10%;  
  padding-right: 10%;
}
</style>
