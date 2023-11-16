<template>
  <div class="main-canvas">
    <div class="mask" v-loading="isUploading"
         element-loading-text="请稍等，录音正在上传中" v-if="isUploading" >
    </div>
    <div class="step-box-bg">
      <div class="step-box" v-if="this.activeStep === 2">
        <el-steps :active="this.activeStep" finish-status="success" align-center>
          <el-step title="量表填写" />
          <el-step title="情绪图片观看" />
          <el-step id="result-step" title="文字朗读" />
          <el-step title="人脸图片描述" />
          <el-step title="机器人访谈" />
          <el-step title="您的结果" />
        </el-steps>
      </div>
      <div class="step-box" v-if="this.activeStep === 1" >
        <el-steps :active="this.activeStep" finish-status="success" align-center>
          <el-step title="情绪图片观看" />
          <el-step id="result-step" title="文字朗读" />
          <el-step title="人脸图片描述" />
          <el-step title="机器人访谈" />
          <el-step title="您的结果" />
        </el-steps>
      </div>
    </div>
    <div class="main-title">文字朗读</div>
    <div class="explain-box">
      <div class="explain-box-left">
        <div class="explain-box-left-text">
          请您大声朗读屏幕上的短文。
        </div>
      </div>
      <div class="explain-box-right">
        <button class="test-mic-button" @click="testMic">测试麦克风</button>
      </div>
    </div>
    <div class="mix-box">
      <div class="back-box">
        <div class="page-button" @click="changeToFirstPage" v-show="this.isLastPage">
          <i class="bi bi-arrow-left-short"></i>
        </div>
      </div>
      <div class="text-box">
        <div class="read-text">
          {{this.showText}}
        </div>
      </div>
      <div class="next-box">
        <div class="page-button" style="margin-left: 2.5vw" v-show="this.isFirstPage" @click="changeToLastPage">
          <i class="bi bi-arrow-right-short"></i>
        </div>
      </div>
    </div>
    <div class="read-button" @click="startRecording" v-show="!isRecording">开始录制</div>
    <div class="read-button" @click="stopRecording" v-show="isRecording">结束朗读</div>
  </div>
</template>

<script>
import { text1, text2, ipAddress } from "../utils.js";
import { ElMessage } from "element-plus";

export default {
  name: "ResizedStep3",
  data(){
    return{
      readText1: text1,
      readText2: text2,
      showText: text1,
      isFirstPage: true,
      isLastPage: false,
      isUploading: false,
      isRecording: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,

      includeQuestionnaire: true,
      activeStep: 2,
    }
  },

  mounted(){
    this.includeQuestionnaire = this.$route.query.includeQuestionnaire;
    if(this.includeQuestionnaire === true){
      this.activeStep = 2;
    }else{
      this.activeStep = 1;
    }
  },

  methods:{
    testMic(){

    },
    changeToFirstPage(){
      this.showText = text1;
      this.isFirstPage = true;
      this.isLastPage = false;
    },
    changeToLastPage(){
      this.showText = text2;
      this.isFirstPage = false;
      this.isLastPage = true;
    },


    startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.isRecording = true;
        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };
        this.mediaRecorder.onstop = () => {
          this.isRecording = false;
          const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
          this.audioUrl = URL.createObjectURL(audioBlob);
          console.log("create:", this.audioUrl);
        };
        this.mediaRecorder.start();
        ElMessage({
          message: '录音已开始',
          type: 'success',
        });
      });
    },

    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
        setTimeout(this.sendAudioToBackend,1000);
      }
    },


    async sendAudioToBackend() {
      this.isUploading = true;
      try {
        const blob = new Blob(this.audioChunks, {type: 'audio/wav'});
        const formData = new FormData();
        formData.append('audio', blob, 'readtext_audio.wav');

        const response = await fetch(`http://${ipAddress}/upload-audio`, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          ElMessage({
            message: '录音已成功上传',
            type: 'success',
          });
          this.isUploading = false;
          this.$router.push({name: 'step4-facedescribe', query: {includeQuestionnaire: this.includeQuestionnaire}});
        } else {
          ElMessage.error('录音上传失败');
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('录音上传失败');
        this.isUploading = false;
      }
    },
  }
}
</script>

<style scoped>
@import "stylesheet/step3-textread.css";
</style>