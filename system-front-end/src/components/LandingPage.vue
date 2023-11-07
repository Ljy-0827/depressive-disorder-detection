<template>
  <div class="main-canvas">
    <img class="banner" src="../assets/setting-pic/landing-page-banner.png" alt="" />
    <div class="main-title">抑郁症多模态检测系统</div>
    <div class="main-description">内容描述占位内容描述占位内容描述内容描述占位内容描述占位内容描述</div>
    <div class="main-button" @click="start">开始检测</div>
    <div class="main-box">
      <div class="box-title">五项测试为您提供全面检测</div>
      <div class="box-card-row" style="margin-left: 5.5vw; margin-top: 4vh">
        <div class="box-card" style="margin-left: 0">
          <div class="icon-bg">
            <i class="bi bi-clipboard-pulse"></i>
          </div>
          <div class="card-title">量表填写</div>
          <div class="card-description">内容描述占位内容描述占位</div>
          <div class="know-more-button">了解更多</div>
        </div>
        <div class="box-card">
          <div class="icon-bg">
            <i class="bi bi-easel2"></i>
          </div>
          <div class="card-title">情绪图片观看</div>
          <div class="card-description">内容描述占位内容描述占位</div>
          <div class="know-more-button">了解更多</div>
        </div>
        <div class="box-card">
          <div class="icon-bg">
            <i class="bi bi-card-heading"></i>
          </div>
          <div class="card-title">文字朗读</div>
          <div class="card-description">内容描述占位内容描述占位</div>
          <div class="know-more-button">了解更多</div>
        </div>
      </div>
      <div class="box-card-row" style="margin-left: 20vw; margin-top: 4vh">
        <div class="box-card" style="margin-left: 0">
          <div class="icon-bg">
            <i class="bi bi-emoji-wink"></i>
          </div>
          <div class="card-title">人脸图片描述</div>
          <div class="card-description">内容描述占位内容描述占位</div>
          <div class="know-more-button">了解更多</div>
        </div>
        <div class="box-card">
          <div class="icon-bg">
            <i class="bi bi-chat-right-dots"></i>
          </div>
          <div class="card-title">机器人访谈</div>
          <div class="card-description">内容描述占位内容描述占位</div>
          <div class="know-more-button">了解更多</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LandingPage",
  data(){
    return{

    }
  },
  methods:{
    start(){
      this.$router.push('/step1_questionnaire');
    }
  }
}
</script>

<style scoped>
@import "stylesheet/landing-page.css";
</style>