<template>
  <div class="main-canvas">
    <div class="mask" v-loading="isUploading"
         element-loading-text="请稍等，数据正在上传中" v-if="isUploading" >
    </div>
    <div class="top-box">
      <div class="back-button" @click="backToLandingPage">
        <i class="bi bi-house-door"></i>
      </div>
      <div class="back-button-text" @click="backToLandingPage">首页</div>
      <div class="step-box-bg">
        <div class="step-box">
          <el-steps :active="0" finish-status="success" align-center>
            <el-step id="result-step" title="量表填写" />
            <el-step title="您的结果" />
          </el-steps>
        </div>
      </div>
    </div>
    <div class="main-title">量表填写</div>
    <div class="explain-box">
      <div class="explain-box-left">
        <div class="explain-box-left-text">
          过去的两周里，您生活中以下症状出现的频率有多少？选择您认为最合适的选项。
        </div>
      </div>
      <div class="explain-box-right">
        <button class="clear-button" @click="clearForm">清空全部</button>
      </div>
    </div>
    <div class="main-carousel">
      <el-form :model="questionnaire" label-position="top">
        <el-carousel indicator-position="none" :autoplay="false" arrow="always">
          <el-carousel-item v-for="(item, index) in questionnaire">
            <div class="question-index">No.{{index +1}}</div>
            <el-form-item  :label="item.question" required>
              <el-radio-group  v-model="this.answer[index]">
                <el-radio v-for="option in item.options" :label="option">
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-carousel-item>
        </el-carousel>
      </el-form>
    </div>

    <div class="carousel-bg"></div>
    <div class="complete-button" @click="submitForm">完成填写</div>

  </div>
</template>

<script>
import {ipAddress, questionnaire} from "../utils.js";
import {ElMessage} from "element-plus";

export default {
  name: "SingleQuestionnaire",
  data(){
    return{
      questionnaire,
      answer:[],
      isUploading: false,
    }
  },
  methods:{
    backToLandingPage(){
      this.$router.push('/');
    },
    postDataToBackend(){
      console.log(this.answer)
      fetch(`http://${ipAddress}/upload-questionnaire-answer`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.answer),
      })
          .then(response => {
            if (response.ok) {
              console.log('questionnaire answer JSON data sent successfully');
              this.isUploading = false;
              this.$router.push('/result');
            } else {
              console.error('Failed to send JSON data to backend.');
            }
          })
          .catch(error => {
            console.error('An error occurred while sending JSON data:', error);
          });
    },

    submitForm() {
      if(this.answer.length === this.questionnaire.length){
        ElMessage({
          message: '量表填写完成',
          type: 'success',
        });
        this.isUploading = true;
        setTimeout(this.postDataToBackend,1000);

      } else{
        ElMessage.error('请您作答全部题目');
      }
    },

    clearForm(){
      this.answer = [];
    }
  }
}
</script>

<style scoped>
@import "stylesheet/single-questionnaire.css";
</style>