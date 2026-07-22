Experiment	Change	Result
R1	autovideosink sync=false	Significant reduction in latency. Buffering warnings disappeared.

Rx pipeline:
build_pipeline()
{
    cat <<EOF
srtsrc uri=srt://${PI_HOST}:${SRT_PORT}
    latency=50
! queue
    max-size-buffers=1
    leaky=downstream
! tsdemux
! h264parse
! avdec_h264
! autovideosink sync=false
EOF
}
Does not work. Removing the queue fixes it.

On the sender side, using a leaky queue before the encoder makes perfect sense because dropping an occasional frame is preferable to increasing latency. On the receiver side, once the stream has been packetised into MPEG-TS, the integrity of the packet sequence matters much more than keeping latency low by discarding data. In other words, the sender should be free to drop frames, but the receiver should never drop transport packets.

=============================================================

(.venv) pi@bz25-rpi-Test:~/raspi-hud/tools/gst-tests $ gst-inspect-1.0 | grep 264
closedcaption:  h264ccextractor: H.264 Closed Caption Extractor
closedcaption:  h264ccinserter: H.264 Closed Caption Inserter
codec2json:  h2642json: H2642json
codectimestamper:  h264timestamper: H.264 timestamper
libav:  avdec_h264: libav H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 decoder
libav:  avmux_ipod: libav iPod H.264 MP4 (MPEG-4 Part 14) muxer
openh264:  openh264dec: OpenH264 video decoder
openh264:  openh264enc: OpenH264 video encoder
rtp:  rtph264depay: RTP H264 depayloader
rtp:  rtph264pay: RTP H264 payloader
typefindfunctions: video/x-h264: h264, x264, 264
uvch264:  uvch264deviceprovider (GstDeviceProviderFactory)
uvch264:  uvch264mjpgdemux: UVC H264 MJPG Demuxer
uvch264:  uvch264src: UVC H264 Source
video4linux2:  v4l2h264dec: V4L2 H264 Decoder
video4linux2:  v4l2h264enc: V4L2 H.264 Encoder
videoparsersbad:  h264parse: H.264 parser
x264:  x264enc: x264 H.264 Encoder

 gst-inspect-1.0 | grep enc
adpcmenc:  adpcmenc: ADPCM encoder
aes:  aesenc: aesenc
alaw:  alawenc: A Law audio encoder
amrnb:  amrnbenc: AMR-NB audio encoder
aom:  av1enc: AV1 Encoder
audiolatency:  audiolatency: AudioLatency
audiovisualizers:  spectrascope: Frequency spectrum scope
avtp:  avtpcrfcheck: Clock Reference Format (CRF) Checker
avtp:  avtpcrfsync: Clock Reference Format (CRF) Synchronizer
bz2:  bz2enc: BZ2 encoder
closedcaption:  line21encoder: Line 21 CC Encoder
coretracers:  latency (GstTracerFactory)
dtls:  dtlsenc: DTLS Encoder
dtls:  dtlssrtpenc: DTLS-SRTP Encoder
dvbsubenc:  dvbsubenc: DVB subtitle encoder
encoding:  encodebin: Encoder Bin
encoding:  encodebin2: Encoder Bin
flac:  flacenc: FLAC audio encoder
gsm:  gsmenc: GSM audio encoder
jpeg:  jpegenc: JPEG image encoder
lame:  lamemp3enc: L.A.M.E. mp3 encoder
lc3:  lc3enc: LC3 Bluetooth Audio encoder
ldac:  ldacenc: Bluetooth LDAC audio encoder
libav:  avdec_h265: libav HEVC (High Efficiency Video Coding) decoder
libav:  avenc_aac: libav AAC (Advanced Audio Coding) encoder
libav:  avenc_ac3: libav ATSC A/52A (AC-3) encoder
libav:  avenc_ac3_fixed: libav ATSC A/52A (AC-3) encoder
libav:  avenc_adpcm_adx: libav SEGA CRI ADX ADPCM encoder
libav:  avenc_adpcm_ima_amv: libav ADPCM IMA AMV encoder
libav:  avenc_adpcm_ima_qt: libav ADPCM IMA QuickTime encoder
libav:  avenc_adpcm_ima_wav: libav ADPCM IMA WAV encoder
libav:  avenc_adpcm_ima_ws: libav ADPCM IMA Westwood encoder
libav:  avenc_adpcm_ms: libav ADPCM Microsoft encoder
libav:  avenc_adpcm_swf: libav ADPCM Shockwave Flash encoder
libav:  avenc_adpcm_yamaha: libav ADPCM Yamaha encoder
libav:  avenc_alac: libav ALAC (Apple Lossless Audio Codec) encoder
libav:  avenc_amv: libav AMV Video encoder
libav:  avenc_aptx: libav aptX (Audio Processing Technology for Bluetooth) encoder
libav:  avenc_aptx_hd: libav aptX HD (Audio Processing Technology for Bluetooth) encoder
libav:  avenc_asv1: libav ASUS V1 encoder
libav:  avenc_asv2: libav ASUS V2 encoder
libav:  avenc_bmp: libav BMP (Windows and OS/2 bitmap) encoder
libav:  avenc_cfhd: libav GoPro CineForm HD encoder
libav:  avenc_cinepak: libav Cinepak encoder
libav:  avenc_cljr: libav Cirrus Logic AccuPak encoder
libav:  avenc_dca: libav DCA (DTS Coherent Acoustics) encoder
libav:  avenc_dnxhd: libav VC3/DNxHD encoder
libav:  avenc_dvvideo: libav DV (Digital Video) encoder
libav:  avenc_eac3: libav ATSC A/52 E-AC-3 encoder
libav:  avenc_ffv1: libav FFmpeg video codec #1 encoder
libav:  avenc_ffvhuff: libav Huffyuv FFmpeg variant encoder
libav:  avenc_flashsv: libav Flash Screen Video encoder
libav:  avenc_flashsv2: libav Flash Screen Video Version 2 encoder
libav:  avenc_flv: libav FLV / Sorenson Spark / Sorenson H.263 (Flash Video) encoder
libav:  avenc_g722: libav G.722 ADPCM encoder
libav:  avenc_g726: libav G.726 ADPCM encoder
libav:  avenc_h261: libav H.261 encoder
libav:  avenc_h263: libav H.263 / H.263-1996 encoder
libav:  avenc_h263p: libav H.263+ / H.263-1998 / H.263 version 2 encoder
libav:  avenc_hap: libav Vidvox Hap encoder
libav:  avenc_huffyuv: libav Huffyuv / HuffYUV encoder
libav:  avenc_jpeg2000: libav JPEG 2000 encoder
libav:  avenc_ljpeg: libav Lossless JPEG encoder
libav:  avenc_mjpeg: libav MJPEG (Motion JPEG) encoder
libav:  avenc_mlp: libav MLP (Meridian Lossless Packing) encoder
libav:  avenc_mp2: libav MP2 (MPEG audio layer 2) encoder
libav:  avenc_mp2fixed: libav MP2 fixed point (MPEG audio layer 2) encoder
libav:  avenc_mpeg1video: libav MPEG-1 video encoder
libav:  avenc_mpeg2video: libav MPEG-2 video encoder
libav:  avenc_mpeg4: libav MPEG-4 part 2 encoder
libav:  avenc_msmpeg4: libav MPEG-4 part 2 Microsoft variant version 3 encoder
libav:  avenc_msmpeg4v2: libav MPEG-4 part 2 Microsoft variant version 2 encoder
libav:  avenc_msrle: libav Microsoft RLE encoder
libav:  avenc_msvideo1: libav Microsoft Video-1 encoder
libav:  avenc_nellymoser: libav Nellymoser Asao encoder
libav:  avenc_opus: libav Opus encoder
libav:  avenc_pam: libav PAM (Portable AnyMap) image encoder
libav:  avenc_pbm: libav PBM (Portable BitMap) image encoder
libav:  avenc_pcx: libav PC Paintbrush PCX image encoder
libav:  avenc_pgm: libav PGM (Portable GrayMap) image encoder
libav:  avenc_pgmyuv: libav PGMYUV (Portable GrayMap YUV) image encoder
libav:  avenc_png: libav PNG (Portable Network Graphics) image encoder
libav:  avenc_ppm: libav PPM (Portable PixelMap) image encoder
libav:  avenc_prores: libav Apple ProRes encoder
libav:  avenc_prores_aw: libav Apple ProRes encoder
libav:  avenc_prores_ks: libav Apple ProRes (iCodec Pro) encoder
libav:  avenc_qoi: libav QOI (Quite OK Image format) image encoder
libav:  avenc_qtrle: libav QuickTime Animation (RLE) video encoder
libav:  avenc_real_144: libav RealAudio 1.0 (14.4K) encoder
libav:  avenc_roq_dpcm: libav id RoQ DPCM encoder
libav:  avenc_roqvideo: libav id RoQ video encoder
libav:  avenc_rpza: libav QuickTime video (RPZA) encoder
libav:  avenc_rv10: libav RealVideo 1.0 encoder
libav:  avenc_rv20: libav RealVideo 2.0 encoder
libav:  avenc_s302m: libav SMPTE 302M encoder
libav:  avenc_sgi: libav SGI image encoder
libav:  avenc_smc: libav QuickTime Graphics (SMC) encoder
libav:  avenc_speedhq: libav NewTek SpeedHQ encoder
libav:  avenc_sunrast: libav Sun Rasterfile image encoder
libav:  avenc_svq1: libav Sorenson Vector Quantizer 1 / Sorenson Video 1 / SVQ1 encoder
libav:  avenc_targa: libav Truevision Targa image encoder
libav:  avenc_tiff: libav TIFF image encoder
libav:  avenc_truehd: libav TrueHD encoder
libav:  avenc_tta: libav TTA (True Audio) encoder
libav:  avenc_wmav1: libav Windows Media Audio 1 encoder
libav:  avenc_wmav2: libav Windows Media Audio 2 encoder
libav:  avenc_wmv1: libav Windows Media Video 7 encoder
libav:  avenc_wmv2: libav Windows Media Video 8 encoder
libav:  avenc_zmbv: libav Zip Motion Blocks Video encoder
libav:  avmux_wav: libav WAV / WAVE (Waveform Audio) muxer (not recommended, use wavenc instead)
libav:  avmux_yuv4mpegpipe: libav YUV4MPEG pipe muxer (not recommended, use y4menc instead)
mpeg2enc:  mpeg2enc: mpeg2enc video encoder
mulaw:  mulawenc: Mu Law audio encoder
multifile:  imagesequencesrc: Image Sequence Source
openaptx:  openaptxenc: Bluetooth aptX/aptX-HD audio encoder using libopenaptx
opengl:  gldifferencematte: Gstreamer OpenGL DifferenceMatte
openh264:  openh264enc: OpenH264 video encoder
openjpeg:  openjpegenc: OpenJPEG JPEG2000 encoder
opus:  opusenc: Opus audio encoder
png:  pngenc: PNG image encoder
pnm:  pnmenc: PNM image encoder
removesilence:  removesilence: RemoveSilence
rtp:  rtpredenc: Redundant Audio Data (RED) Encoder
rtp:  rtpulpfecenc: RTP FEC Encoder
rtpmanager:  rtpst2022-1-fecenc: SMPTE 2022-1 FEC encoder
sbc:  sbcenc: Bluetooth SBC audio encoder
sctp:  sctpenc: SCTP Encoder
siren:  sirenenc: Siren Encoder element
speex:  speexenc: Speex audio encoder
srtp:  srtpenc: SRTP encoder
subenc:  srtenc: Srt encoder
subenc:  webvttenc: WebVTT encoder
svtav1:  svtav1enc: SvtAv1Enc
theora:  theoraenc: Theora video encoder
twolame:  twolamemp2enc: TwoLAME mp2 encoder
video4linux2:  v4l2h264enc: V4L2 H.264 Encoder
video4linux2:  v4l2jpegenc: V4L2 JPEG Encoder
video4linux2:  v4l2video31jpegenc: V4L2 JPEG Encoder
voaacenc:  voaacenc: AAC audio encoder
voamrwbenc:  voamrwbenc: AMR-WB audio encoder
vorbis:  vorbisenc: Vorbis audio encoder
vpx:  vp8enc: On2 VP8 Encoder
vpx:  vp9enc: On2 VP9 Encoder
wavenc:  wavenc: WAV audio muxer
wavpack:  wavpackenc: Wavpack audio encoder
webp:  webpenc: WEBP image encoder
x264:  x264enc: x264 H.264 Encoder
x265:  x265enc: x265enc
y4menc:  y4menc: YUV4MPEG video encoder

gst-inspect-1.0 v4l2h264enc
Factory Details:
  Rank                     primary + 1 (257)
  Long-name                V4L2 H.264 Encoder
  Klass                    Codec/Encoder/Video/Hardware
  Description              Encode H.264 video streams via V4L2 API
  Author                   ayaka <ayaka@soulik.info>
  Documentation            https://gstreamer.freedesktop.org/documentation/video4linux2/v4l2h264enc.html

Plugin Details:
  Name                     video4linux2
  Description              elements for Video 4 Linux
  Filename                 /usr/lib/aarch64-linux-gnu/gstreamer-1.0/libgstvideo4linux2.so
  Version                  1.26.2
  License                  LGPL
  Source module            gst-plugins-good
  Documentation            https://gstreamer.freedesktop.org/documentation/video4linux2/
  Source release date      2025-05-29
  Binary package           GStreamer Good Plugins (Debian)
  Origin URL               https://tracker.debian.org/pkg/gst-plugins-good1.0

GObject
 +----GInitiallyUnowned
       +----GstObject
             +----GstElement
                   +----GstVideoEncoder
                         +----GstV4l2VideoEnc
                               +----GstV4l2H264Enc
                                     +----v4l2h264enc

Implemented Interfaces:
  GstPreset

Element Flags:

Pad Templates:
  SINK template: 'sink'
    Availability: Always
    Capabilities:
      video/x-raw(memory:DMABuf)
                 format: DMA_DRM
             drm-format: { (string)YU12, (string)YV12, (string)NV12, (string)NV21, (string)RG16, (string)BG24, (string)RG24, (string)AB24, (string)XR24, (string)YUYV, (string)YVYU, (string)UYVY, (string)VYUY }
                  width: [ 1, 32768 ]
                 height: [ 1, 32768 ]
              framerate: [ 0/1, 2147483647/1 ]
      video/x-raw(memory:DMABuf, format:Interlaced)
                 format: DMA_DRM
             drm-format: { (string)YU12, (string)YV12, (string)NV12, (string)NV21, (string)RG16, (string)BG24, (string)RG24, (string)AB24, (string)XR24, (string)YUYV, (string)YVYU, (string)UYVY, (string)VYUY }
                  width: [ 1, 32768 ]
                 height: [ 1, 32768 ]
              framerate: [ 0/1, 2147483647/1 ]
         interlace-mode: alternate
      video/x-raw
                 format: { (string)I420, (string)YV12, (string)NV12, (string)NV21, (string)RGB16, (string)RGB, (string)BGR, (string)RGBA, (string)BGRx, (string)BGRA, (string)YUY2, (string)YVYU, (string)UYVY }
                  width: [ 1, 32768 ]
                 height: [ 1, 32768 ]
              framerate: [ 0/1, 2147483647/1 ]
      video/x-raw(format:Interlaced)
                 format: { (string)I420, (string)YV12, (string)NV12, (string)NV21, (string)RGB16, (string)RGB, (string)BGR, (string)RGBA, (string)BGRx, (string)BGRA, (string)YUY2, (string)YVYU, (string)UYVY }
                  width: [ 1, 32768 ]
                 height: [ 1, 32768 ]
              framerate: [ 0/1, 2147483647/1 ]
         interlace-mode: alternate
  
  SRC template: 'src'
    Availability: Always
    Capabilities:
      video/x-h264
          stream-format: byte-stream
              alignment: au
                  level: { (string)1, (string)1b, (string)1.1, (string)1.2, (string)1.3, (string)2, (string)2.1, (string)2.2, (string)3, (string)3.1, (string)3.2, (string)4, (string)4.1, (string)4.2, (string)5, (string)5.1 }
                profile: { (string)baseline, (string)constrained-baseline, (string)main, (string)high }

Element has no clocking capabilities.
Element has no URI handling capabilities.

Pads:
  SINK: 'sink'
    Pad Template: 'sink'
  SRC: 'src'
    Pad Template: 'src'

Element Properties:

  capture-io-mode     : Capture I/O mode (matches src pad)
                        flags: readable, writable
                        Enum "GstV4l2IOMode" Default: 0, "auto"
                           (0): auto             - GST_V4L2_IO_AUTO
                           (1): rw               - GST_V4L2_IO_RW
                           (2): mmap             - GST_V4L2_IO_MMAP
                           (3): userptr          - GST_V4L2_IO_USERPTR
                           (4): dmabuf           - GST_V4L2_IO_DMABUF
                           (5): dmabuf-import    - GST_V4L2_IO_DMABUF_IMPORT
  
  device              : Device location
                        flags: readable
                        String. Default: "/dev/video11"
  
  device-fd           : File descriptor of the device
                        flags: readable
                        Integer. Range: -1 - 2147483647 Default: -1 
  
  device-name         : Name of the device
                        flags: readable
                        String. Default: null
  
  extra-controls      : Extra v4l2 controls (CIDs) for the device
                        flags: readable, writable
                        Boxed pointer of type "GstStructure"
  
  min-force-key-unit-interval: Minimum interval between force-keyunit requests in nanoseconds
                        flags: readable, writable
                        Unsigned Integer64. Range: 0 - 18446744073709551615 Default: 0 
  
  name                : The name of the object
                        flags: readable, writable
                        String. Default: "v4l2h264enc0"
  
  output-io-mode      : Output side I/O mode (matches sink pad)
                        flags: readable, writable
                        Enum "GstV4l2IOMode" Default: 0, "auto"
                           (0): auto             - GST_V4L2_IO_AUTO
                           (1): rw               - GST_V4L2_IO_RW
                           (2): mmap             - GST_V4L2_IO_MMAP
                           (3): userptr          - GST_V4L2_IO_USERPTR
                           (4): dmabuf           - GST_V4L2_IO_DMABUF
                           (5): dmabuf-import    - GST_V4L2_IO_DMABUF_IMPORT
  
  parent              : The parent of the object
                        flags: readable, writable
                        Object of type "GstObject"
  
  qos                 : Handle Quality-of-Service events from downstream
                        flags: readable, writable
  
