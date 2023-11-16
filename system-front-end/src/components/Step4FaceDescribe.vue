<template>
  <div class="step-box-bg">
    <div class="step-box" v-if="this.activeStep === 3">
      <el-steps :active="this.activeStep" finish-status="success" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step id="result-step" title="人脸图片描述" />
        <el-step title="机器人访谈" />
        <el-step title="您的结果" />
      </el-steps>
    </div>
    <div class="step-box" v-if="this.activeStep === 2" >
      <el-steps :active="this.activeStep" finish-status="success" align-center>
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step id="result-step" title="人脸图片描述" />
        <el-step title="机器人访谈" />
        <el-step title="您的结果" />
      </el-steps>
    </div>
  </div>
  <div class="main-title">人脸图片描述</div>
  <div class="explain-box">
    <div class="explain-box-left">
      <div class="explain-box-left-text">
        请您认真观看并描述屏幕上的图片，请尽可能多地说出您理解的内容。
      </div>
    </div>
    <div class="explain-box-right">
      <button class="open-camera-button" v-if="!isCameraOpen" @click="openCamera">打开音视频</button>
      <div class="open-camera-countdown" v-if="!isCameraOpen">音视频将在{{this.countdown}}秒后自动开启</div>
      <video ref="videoElement" autoplay class="camera" v-show="isCameraOpen" muted></video>
    </div>
  </div>
  <div class="pic-box">
    <img src="../assets/watch-images/face-1.png" class="picture" v-show="this.describePic === 'pic1'">
    <img src="../assets/watch-images/face-2.png" class="picture" v-show="this.describePic === 'pic2'">
    <img src="../assets/watch-images/face-3.png" class="picture" v-show="this.describePic === 'pic3'">
  </div>
  <div class="complete-button" @click="startDescribe" v-show="this.describePic === '0'">开始描述</div>
  <div class="complete-button" @click="nextPicture" v-show="this.describePic === 'pic1' || this.describePic === 'pic2'">下一张</div>
  <div class="complete-button" @click="finishDescribe" v-show="this.describePic === 'pic3'">结束描述</div>
</template>

<script>
import {ipAddress} from "../utils.js";
import {ElMessage} from "element-plus";

export default {
  name: "Step4FaceDescribe",
  data(){
    return{
      isCameraOpen: false,
      describePic: '0',
      isRecording: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,
      isUploading: false,
      countdown: 3,
      timer: null,

      activeStep: 3,
      includeQuestionnaire: true,
    }
  },

  mounted() {
    this.includeQuestionnaire = this.$route.query.includeQuestionnaire;
    if(this.includeQuestionnaire === true){
      this.activeStep = 3;
    }else{
      this.activeStep = 2;
    }
    this.startCountdown();
  },

  methods:{
    startCountdown() {
      this.countdown = 3;
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          clearInterval(this.timer);  // 清除计时器
          this.openCamera();
        }
      }, 1000);
    },

    async openCamera() {
      console.log(this.isRecording);
      this.isCameraOpen = true;

      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        this.$refs.videoElement.srcObject = this.mediaStream;

        ElMessage({
          message: '摄像头连接成功',
          type: 'success',
        });
      } catch (error) {
        ElMessage.error('无法访问摄像头');
        console.error('无法访问摄像头', error);
      }
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
        this.isUploading = true;
        setTimeout(this.sendAudioToBackend,1000);
      }
    },

    async sendAudioToBackend() {
      try {
        const blob = new Blob(this.audioChunks, {type: 'audio/wav'});
        const formData = new FormData();
        formData.append('audio', blob, 'facedescribe_audio.wav');

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
          this.$router.push({name: 'step5-interview', query: {includeQuestionnaire: this.includeQuestionnaire}});
        } else {
          ElMessage.error('录音上传失败');
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('录音上传失败');
        this.isUploading = false;
      }
    },

    startDescribe(){
      this.startRecording();
      this.describePic = 'pic1';
    },

    nextPicture(){
      if(this.describePic === 'pic1'){
        this.describePic = 'pic2';
      }else if(this.describePic === 'pic2'){
        this.describePic = 'pic3';
      }
    },

    finishDescribe(){
      this.describePic = '0';
      this.stopRecording();
    }
  }
}
</script>

<style scoped>
@import "stylesheet/step4-facedescribe.css";
</style>