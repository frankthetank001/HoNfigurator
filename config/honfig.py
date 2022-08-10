import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import stat
from os.path import exists

conf1=["SetSave","_testTrialAccount","false","0"]
conf2=["SetSave","cam_alwaysThirdPerson","false","0"]
conf3=["SetSave","cam_fov","90.0000","0"]
conf4=["SetSave","cam_smoothAnglesHalfLife","0.0500","0"]
conf5=["SetSave","cam_smoothPositionHalfLife","0.1000","0"]
conf6=["SetSave","cc_curGameChannel","","0"]
conf7=["SetSave","cc_DisableNotifications","false","0"]
conf8=["SetSave","cc_DisableNotificationsInGame","false","0"]
conf9=["SetSave","cc_notificationDuration","10","0"]
conf10=["SetSave","cc_showBuddyAddNotification","true","0"]
conf11=["SetSave","cc_showBuddyConnectionNotification","true","0"]
conf12=["SetSave","cc_showBuddyDisconnectionNotification","true","0"]
conf13=["SetSave","cc_showBuddyJoinGameNotification","true","0"]
conf14=["SetSave","cc_showBuddyLeaveGameNotification","true","0"]
conf15=["SetSave","cc_showBuddyRemovedNotification","true","0"]
conf16=["SetSave","cc_showBuddyRequestNotification","true","0"]
conf17=["SetSave","cc_showClanAddNotification","true","0"]
conf18=["SetSave","cc_showClanConnectionNotification","true","0"]
conf19=["SetSave","cc_showClanDisconnectionNotification","true","0"]
conf20=["SetSave","cc_showClanJoinGameNotification","true","0"]
conf21=["SetSave","cc_showClanLeaveGameNotification","true","0"]
conf22=["SetSave","cc_showClanMessageNotification","true","0"]
conf23=["SetSave","cc_showClanRankNotification","true","0"]
conf24=["SetSave","cc_showClanRemoveNotification","true","0"]
conf25=["SetSave","cc_showGameInvites","true","0"]
conf26=["SetSave","cc_showIMNotification","true","0"]
conf27=["SetSave","cc_showNewPatchNotification","true","0"]
conf28=["SetSave","cc_TMMMatchFidelity","0","0"]
conf29=["SetSave","cg_censorChat","true","0"]
conf30=["SetSave","cg_disableReleasedShaderCache","false","0"]
conf31=["SetSave","cg_healthLerpMode","2","0"]
conf32=["SetSave","cg_healthLerpMode2MaxMultipler","4","0"]
conf33=["SetSave","cg_healthLerpMode2Multipler","0.3330","0"]
conf34=["SetSave","cg_muteAnnouncerVoice","false","0"]
conf35=["SetSave","chat_connectTimeout","3","0"]
conf36=["SetSave","chat_gameLobbyChatToggle","274","0"]
conf37=["SetSave","chat_maxReconnectAttempts","5","0"]
conf38=["SetSave","chat_showChatTimestamps","false","0"]
conf39=["SetSave","cl_connectionID","0","0"]
conf40=["SetSave","cl_infoRequestRate","30.0000","0"]
conf41=["SetSave","cl_packetSendFPS","30","0"]
conf42=["SetSave","cl_printStateStringChanges","false","0"]
conf43=["SetSave","cl_Rap2Enable","false","0"]
conf44=["SetSave","con_alpha","1.0000","0"]
conf45=["SetSave","con_bgColor","0.5000,0.5000,0.5000","0"]
conf46=["SetSave","con_color","1.0000,1.0000,1.0000","0"]
conf47=["SetSave","con_font","system_medium","0"]
conf48=["SetSave","con_height","1.0000","0"]
conf49=["SetSave","con_notify","false","0"]
conf50=["SetSave","con_notifyLines","8","0"]
conf51=["SetSave","con_notifyTime","4000","0"]
conf52=["SetSave","con_prompt",">","0"]
conf53=["SetSave","con_tabWidth","5","0"]
conf54=["SetSave","con_terminalOut","false","0"]
conf55=["SetSave","con_toggleTime","200","0"]
conf56=["SetSave","con_wordWrap","false","0"]
conf57=["SetSave","cow_precache","false","0"]
conf58=["SetSave","d3d_altCursor","false","0"]
conf59=["SetSave","d3d_exclusive","true","0"]
conf60=["SetSave","d3d_flush","1","0"]
conf61=["SetSave","d3d_hardwareRaster","true","0"]
conf62=["SetSave","d3d_hardwareTL","true","0"]
conf63=["SetSave","d3d_modeExNew","true","0"]
conf64=["SetSave","d3d_presentInterval","0","0"]
conf65=["SetSave","d3d_pure","true","0"]
conf66=["SetSave","d3d_software","false","0"]
conf67=["SetSave","d3d_tripleBuffering","false","0"]
conf68=["SetSave","d_debugRendererFont","system_medium","0"]
conf69=["SetSave","d_debugRendererModel","/core/null/null.mdf","0"]
conf70=["SetSave","fs_disablemods","false","0"]
conf71=["SetSave","gfx_depthFirst","false","0"]
conf72=["SetSave","gfx_foliage","true","0"]
conf73=["SetSave","gfx_sky","false","0"]
conf74=["SetSave","gui_colorscale1_1","1.6000,1.8000,1.7000,1.0000","0"]
conf75=["SetSave","host_affinity","0","0"]
conf76=["SetSave","host_backuplanguage","en","0"]
conf77=["SetSave","host_benchmarkControlsProfiling","false","0"]
conf78=["SetSave","host_cloudAutoDownload","false","0"]
conf79=["SetSave","host_cloudAutoUpload","false","0"]
conf80=["SetSave","host_cloudLastModified","","0"]
conf81=["SetSave","host_cloudLastModifiedUser","","0"]
conf82=["SetSave","host_debugInit","false","0"]
conf83=["SetSave","host_dnsResolveFrequency","60000","0"]
conf84=["SetSave","host_dynamicResReload","false","0"]
conf85=["SetSave","host_language","en","0"]
conf86=["SetSave","host_maximumFPS","240","0"]
conf87=["SetSave","host_resReloadDelay","1","0"]
conf88=["SetSave","host_runOnce","","0"]
conf89=["SetSave","host_screenshotFormat","jpg","0"]
conf90=["SetSave","host_screenshotQuality","90","0"]
conf91=["SetSave","host_vidDriver","vid_d3d9","0"]
conf92=["SetSave","http_defaultConnectTimeout","15","0"]
conf93=["SetSave","http_defaultLowSpeedLimit","10","0"]
conf94=["SetSave","http_defaultLowSpeedTimeout","25","0"]
conf95=["SetSave","http_defaultTimeout","30","0"]
conf96=["SetSave","http_printDebugInfo","false","0"]
conf97=["SetSave","http_upload_tunnel_count","1","0"]
conf98=["SetSave","http_useCompression","true","0"]
conf99=["SetSave","input_joyControlCursor","false","0"]
conf100=["SetSave","input_joyCursorSpeed","150.0000","0"]
conf101=["SetSave","input_joyCursorX","3","0"]
conf102=["SetSave","input_joyCursorY","4","0"]
conf103=["SetSave","input_joyDeadZoneR","0.1000","0"]
conf104=["SetSave","input_joyDeadZoneU","0.1000","0"]
conf105=["SetSave","input_joyDeadZoneV","0.1000","0"]
conf106=["SetSave","input_joyDeadZoneX","0.1000","0"]
conf107=["SetSave","input_joyDeadZoneY","0.1000","0"]
conf108=["SetSave","input_joyDeadZoneZ","0.1000","0"]
conf109=["SetSave","input_joyDeviceID","-1","0"]
conf110=["SetSave","input_joyGainR","1.0000","0"]
conf111=["SetSave","input_joyGainU","1.0000","0"]
conf112=["SetSave","input_joyGainV","1.0000","0"]
conf113=["SetSave","input_joyGainX","1.0000","0"]
conf114=["SetSave","input_joyGainY","1.0000","0"]
conf115=["SetSave","input_joyGainZ","1.0000","0"]
conf116=["SetSave","input_joyInvertR","false","0"]
conf117=["SetSave","input_joyInvertU","false","0"]
conf118=["SetSave","input_joyInvertV","false","0"]
conf119=["SetSave","input_joyInvertX","false","0"]
conf120=["SetSave","input_joyInvertY","false","0"]
conf121=["SetSave","input_joyInvertZ","false","0"]
conf122=["SetSave","input_joySensitivityR","1.0000","0"]
conf123=["SetSave","input_joySensitivityU","1.0000","0"]
conf124=["SetSave","input_joySensitivityV","1.0000","0"]
conf125=["SetSave","input_joySensitivityX","1.0000","0"]
conf126=["SetSave","input_joySensitivityY","1.0000","0"]
conf127=["SetSave","input_joySensitivityZ","1.0000","0"]
conf128=["SetSave","input_mouseInvertX","false","0"]
conf129=["SetSave","input_mouseInvertY","false","0"]
conf130=["SetSave","input_mouseSensitivity","1.0000","0"]
conf131=["SetSave","input_mouseSensitivityX","1.0000","0"]
conf132=["SetSave","input_mouseSensitivityY","1.0000","0"]
conf133=["SetSave","key_splitAlt","false","0"]
conf134=["SetSave","key_splitCtrl","false","0"]
conf135=["SetSave","key_splitEnter","false","0"]
conf136=["SetSave","key_splitShift","false","0"]
conf137=["SetSave","key_splitWin","false","0"]
conf138=["SetSave","login_invisible","false","0"]
conf139=["SetSave","man_allowCPUs","","0"]
conf140=["SetSave","man_autoServersPerCPU","0","0"]
conf141=["SetSave","man_broadcastSlaves","true","0"]
conf142=["SetSave","man_cowServerPort","11234","0"]
conf143=["SetSave","man_cowVoiceProxyPort","11434","0"]
conf144=["SetSave","man_enableProxy","false","0"]
conf145=["SetSave","man_endServerPort","11335","0"]
conf146=["SetSave","man_idleTarget","1","0"]
conf147=["SetSave","man_logPeriod","5000","0"]
conf148=["SetSave","man_logUploadInterval","60","0"]
conf149=["SetSave","man_masterLogin","","0"]
conf150=["SetSave","man_masterPassword","","0"]
conf151=["SetSave","man_maxServers","-1","0"]
conf152=["SetSave","man_numSlaveAccounts","10","0"]
conf153=["SetSave","man_port","1135","0"]
conf154=["SetSave","man_resetOnCowError","true","0"]
conf155=["SetSave","man_resubmitStats","true","0"]
conf156=["SetSave","man_startServerPort","11235","0"]
conf157=["SetSave","man_uploadReplays","true","0"]
conf158=["SetSave","man_voiceProxyEndPort","11535","0"]
conf159=["SetSave","man_voiceProxyStartPort","11435","0"]
conf160=["SetSave","mem_font","system_medium","0"]
conf161=["SetSave","model_quality","high","0"]
conf162=["SetSave","net_FPS","20","0"]
conf163=["SetSave","net_maxBPS","20000","0"]
conf164=["SetSave","net_maxPacketSize","1300","0"]
conf165=["SetSave","prof_font","system_medium","0"]
conf166=["SetSave","sample_frontLoadSound","true","0"]
conf167=["SetSave","scene_entityDrawDistance","6500.0000","0"]
conf168=["SetSave","scene_farClip","3000.0000","0"]
conf169=["SetSave","scene_farClipCalcDebug","false","0"]
conf170=["SetSave","scene_foliageDrawDistance","3000.0000","0"]
conf171=["SetSave","scene_rimAlpha","0.5000,0.5000,0.5000","0"]
conf172=["SetSave","sound_bufferSize","-1","0"]
conf173=["SetSave","sound_disable","false","0"]
conf174=["SetSave","sound_disableRecording","false","0"]
conf175=["SetSave","sound_driver","0","0"]
conf176=["SetSave","sound_interfaceVolume","0.7000","0"]
conf177=["SetSave","sound_masterVolume","1.0000","0"]
conf178=["SetSave","sound_maxVariations","16","0"]
conf179=["SetSave","sound_mixrate","44100","0"]
conf180=["SetSave","sound_mono","false","0"]
conf181=["SetSave","sound_monoBoost","1.0000","0"]
conf182=["SetSave","sound_monoToStereoVolume","0.8000","0"]
conf183=["SetSave","sound_musicVolume","0.2000","0"]
conf184=["SetSave","sound_mute","false","0"]
conf185=["SetSave","sound_muteMusic","false","0"]
conf186=["SetSave","sound_numChannels","128","0"]
conf187=["SetSave","sound_output","","0"]
conf188=["SetSave","sound_pitchShift","true","0"]
conf189=["SetSave","sound_prologic","false","0"]
conf190=["SetSave","sound_recording_driver","0","0"]
conf191=["SetSave","sound_resampler","2","0"]
conf192=["SetSave","sound_sfxVolume","0.6000","0"]
conf193=["SetSave","sound_speakerModeMono","false","0"]
conf194=["SetSave","sound_speakerModeStereo","true","0"]
conf195=["SetSave","sound_stereo","false","0"]
conf196=["SetSave","sound_stereoBoost","1.0000","0"]
conf197=["SetSave","sound_updateFrameFrequncyMs","5000","0"]
conf198=["SetSave","sound_useCompressedSamples","true","0"]
conf199=["SetSave","sound_voiceChatVolume","1.0000","0"]
conf200=["SetSave","sound_voiceMicMuted","false","0"]
conf201=["SetSave","sv_logcollection_highping_interval","120000","0"]
conf202=["SetSave","sv_logcollection_highping_reportclientnum","1","0"]
conf203=["SetSave","sv_logcollection_highping_value","100","0"]
conf204=["SetSave","sv_remoteAdmins","","0"]
conf205=["SetSave","svr_adminPassword","","0"]
conf206=["SetSave","svr_authTimeout","10000","0"]
conf207=["SetSave","svr_broadcast","false","0"]
conf208=["SetSave","svr_chatConnectedTimeout","30000","0"]
conf209=["SetSave","svr_chatConnectTimeout","10000","0"]
conf210=["SetSave","svr_chatReconnectDelay","15000","0"]
conf211=["SetSave","svr_clientConnectedTimeout","30000","0"]
conf212=["SetSave","svr_clientConnectingTimeout","30000","0"]
conf213=["SetSave","svr_clientRefreshUpgradesThrottle","5000","0"]
conf214=["SetSave","svr_clientReminderInterval","5000","0"]
conf215=["SetSave","svr_clientWarnTimeout","2000","0"]
conf216=["SetSave","svr_connectReqPeriod","3000","0"]
conf217=["SetSave","svr_connectReqThreshold","10","0"]
conf218=["SetSave","svr_desc","","0"]
conf219=["SetSave","svr_diagnosticsInterval","5000","0"]
conf220=["SetSave","svr_firstSnapshotRetryInterval","5000","0"]
conf221=["SetSave","svr_gameFPS","20","0"]
conf222=["SetSave","svr_heartbeatInterval","60000","0"]
conf223=["SetSave","svr_ip","","0"]
conf224=["SetSave","svr_kickBanCount","2","0"]
conf225=["SetSave","svr_location","","0"]
conf226=["SetSave","svr_login","","0"]
conf227=["SetSave","svr_longFrameWarnTime","125","0"]
conf228=["SetSave","svr_masterServerAuthScript","/server_requester.php","0"]
conf229=["SetSave","svr_maxbps","20000","0"]
conf230=["SetSave","svr_maxClients","-1","0"]
conf231=["SetSave","svr_maxFramesPerHostFrame","2","0"]
conf232=["SetSave","svr_maxReminders","5","0"]
conf233=["SetSave","svr_minSnapshotCompressSize","256","0"]
conf234=["SetSave","svr_minStateStringCompressSize","256","0"]
conf235=["SetSave","svr_name","Configure Me","0"]
conf236=["SetSave","svr_password","","0"]
conf237=["SetSave","svr_port","11235","0"]
conf238=["SetSave","svr_proxyLocalVoicePort","11435","0"]
conf239=["SetSave","svr_proxyPort","11235","0"]
conf240=["SetSave","svr_proxyRemoteVoicePort","21435","0"]
conf241=["SetSave","svr_reliableUnresponsiveTime","1500","0"]
conf242=["SetSave","svr_replaysegment_package_size","2","0"]
conf243=["SetSave","svr_replaysegment_pressure","1","0"]
conf244=["SetSave","svr_requestSessionCookieTimeout","10000","0"]
conf245=["SetSave","svr_requireAuthentication","true","0"]
conf246=["SetSave","svr_showLongServerFrames","true","0"]
conf247=["SetSave","svr_snapshotCompress","false","0"]
conf248=["SetSave","svr_stateStringCompress","true","0"]
conf249=["SetSave","svr_submitStats","true","0"]
conf250=["SetSave","svr_userPassword","","0"]
conf251=["SetSave","svr_voicePortEnd","11535","0"]
conf252=["SetSave","svr_voicePortStart","11435","0"]
conf253=["SetSave","sys_autoSaveConfig","true","0"]
conf254=["SetSave","sys_autoSaveDump","false","0"]
conf255=["SetSave","sys_dedicatedServerCrashReport","false","0"]
conf256=["SetSave","sys_keepDumpAfterUpload","true","1"]
conf257=["SetSave","sys_keepOldDumpsOnStartup","false","0"]
conf258=["SetSave","ui_drawGrid","false","0"]
conf259=["SetSave","ui_modelPanelCursorRotAnglePerPixel","0.5000","0"]
conf260=["SetSave","ui_modelPanelCursorRotTime","200","0"]
conf261=["SetSave","ui_translateLabels","true","0"]
conf262=["SetSave","ui_webPanelDebug","false","0"]
conf263=["SetSave","ui_widgetTreeFont","system_medium","0"]
conf264=["SetSave","upd_checkForUpdates","false","0"]
conf265=["SetSave","upd_ftpActive","false","0"]
conf266=["SetSave","upd_maxActiveDownloads","6","0"]
conf267=["SetSave","vid_alphaTestRef","90","0"]
conf268=["SetSave","vid_antialiasing","0,0","0"]
conf269=["SetSave","vid_aspect","","0"]
conf270=["SetSave","vid_bpp","32","0"]
conf271=["SetSave","vid_chameleonEnviromentCopy","false","0"]
conf272=["SetSave","vid_chameleonNumPixelLookUps","50","0"]
conf273=["SetSave","vid_chameleonSaturationMax","1.0000","0"]
conf274=["SetSave","vid_chameleonSaturationMin","0.0000","0"]
conf275=["SetSave","vid_chameleonValueMax","1.0000","0"]
conf276=["SetSave","vid_chameleonValueMin","0.5000","0"]
conf277=["SetSave","vid_cullGroundSprites","true","0"]
conf278=["SetSave","vid_cullGroundSpritesSize","5000.0000","0"]
conf279=["SetSave","vid_dynamicLights","true","0"]
conf280=["SetSave","vid_enableGuiChannels","true","0"]
conf281=["SetSave","vid_foliageAlphaTestRef","90","0"]
conf282=["SetSave","vid_foliageAlphaTestRef2","90","0"]
conf283=["SetSave","vid_foliageDensity","1.0000","0"]
conf284=["SetSave","vid_foliageFalloffDistance","100.0000","0"]
conf285=["SetSave","vid_foliageMinDensity","0.0000","0"]
conf286=["SetSave","vid_foliageMinHeight","20.0000","0"]
conf287=["SetSave","vid_foliageMinScale","0.2500","0"]
conf288=["SetSave","vid_foliageMinWidth","5.0000","0"]
conf289=["SetSave","vid_foliageRenderType","0","0"]
conf290=["SetSave","vid_fullscreen","true","0"]
conf291=["SetSave","vid_gamma","1.1000","0"]
conf292=["SetSave","vid_geometryPreload","true","0"]
conf293=["SetSave","vid_lodBias","0","0"]
conf294=["SetSave","vid_lodCurve","2","0"]
conf295=["SetSave","vid_lodForce","-1","0"]
conf296=["SetSave","vid_lodUse","true","0"]
conf297=["SetSave","vid_maxDynamicLights","4","0"]
conf298=["SetSave","vid_meshForceNonBlendedDeform","false","0"]
conf299=["SetSave","vid_meshGPUDeform","true","0"]
conf300=["SetSave","vid_motionBlur","false","0"]
conf301=["SetSave","vid_outlines","true","0"]
conf302=["SetSave","vid_postEffectMipmaps","true","0"]
conf303=["SetSave","vid_postEffects","true","0"]
conf304=["SetSave","vid_precreateDynamicBuffers","false","0"]
conf305=["SetSave","vid_reflectionMapSize","1","0"]
conf306=["SetSave","vid_reflections","false","0"]
conf307=["SetSave","vid_refreshRate","32","0"]
conf308=["SetSave","vid_resolution","2560,1080","0"]
conf309=["SetSave","vid_sceneBuffer","true","0"]
conf310=["SetSave","vid_sceneBufferMipmap","true","0"]
conf311=["SetSave","vid_shader_Precache","true","0"]
conf312=["SetSave","vid_shaderCRC","true","0"]
conf313=["SetSave","vid_shaderDebug","false","0"]
conf314=["SetSave","vid_shaderFalloffQuality","0","0"]
conf315=["SetSave","vid_shaderFogQuality","0","0"]
conf316=["SetSave","vid_shaderLegacyCompiler","false","0"]
conf317=["SetSave","vid_shaderLightingQuality","0","0"]
conf318=["SetSave","vid_shaderPartialPrecision","false","0"]
conf319=["SetSave","vid_shaderRimLighting","false","0"]
conf320=["SetSave","vid_shaderSmoothSelfOcclude","true","0"]
conf321=["SetSave","vid_shaderTexkill","false","0"]
conf322=["SetSave","vid_shaderWaterQuality","1","0"]
conf323=["SetSave","vid_shadowDrawDistance","3000.0000","0"]
conf324=["SetSave","vid_shadowFalloffDistance","1000.0000","0"]
conf325=["SetSave","vid_shadowLeak","0.1000","0"]
conf326=["SetSave","vid_shadowmapFilterWidth","1","0"]
conf327=["SetSave","vid_shadowmapSize","1024","0"]
conf328=["SetSave","vid_shadowmapType","1","0"]
conf329=["SetSave","vid_shadows","true","0"]
conf330=["SetSave","vid_specularLookup","false","0"]
conf331=["SetSave","vid_terrainAlphamap","false","0"]
conf332=["SetSave","vid_terrainDerepeat","false","0"]
conf333=["SetSave","vid_terrainShadows","true","0"]
conf334=["SetSave","vid_terrainSinglePass","true","0"]
conf335=["SetSave","vid_textureAutogenMipmaps","false","0"]
conf336=["SetSave","vid_textureCompression","true","0"]
conf337=["SetSave","vid_textureDownsize","0","0"]
conf338=["SetSave","vid_textureFiltering","2","0"]
conf339=["SetSave","vid_textureMaxSize","4096","0"]
conf340=["SetSave","vid_texturePreload","true","0"]
conf341=["SetSave","vid_treeSmoothNormals","false","0"]
conf342=["SetSave","vid_waterDisMapSize","1","0"]
conf343=["SetSave","voice_audioDampen","0.4000","0"]
conf344=["SetSave","voice_debug","false","0"]
conf345=["SetSave","voice_disabled","false","0"]
conf346=["SetSave","voice_micOnLevel","20.0000","0"]
conf347=["SetSave","voice_micOnTime","1000","0"]
conf348=["SetSave","voice_pushToTalk","true","0"]
conf349=["SetSave","voice_volume","1.0000","0"]
conf350=["SetSave","water_DirectionSmoothing","0.2500","0"]
conf351=["SetSave","water_drawAboveGroundOnly","true","0"]
conf352=["SetSave","water_heightDifference","10.0000","0"]
conf353=["SetSave","water_smoothEdges","false","0"]
conf354=["SetSave","water_smoothHeight","false","0"]
conf355=["SetSave","water_smoothSamples","10","0"]
conf356=["SetSave","g_perks","true","0"]
conf357=["SetSave","login_useSRP","false","0"]
conf358=["SetSave","svr_ignoreConnectionIDForReconnect","true","0"]
conf359=["SetSave","svr_version","4.10.1","0"]
conf360=["SetSave","svr_chatAddress","","0"]

class honfig():
    def __init__(self):
        return
    def getconf1(self):
        return conf1	
    def getconf2(self):
        return conf2		
    def getconf3(self):
        return conf3		
    def getconf4(self):
        return conf4		
    def getconf5(self):
        return conf5		
    def getconf6(self):
        return conf6		
    def getconf7(self):
        return conf7		
    def getconf8(self):
        return conf8		
    def getconf9(self):
        return conf9		
    def getconf10(self):
        return conf10		
    def getconf11(self):
        return conf11		
    def getconf12(self):
        return conf12		
    def getconf13(self):
        return conf13		
    def getconf14(self):
        return conf14		
    def getconf15(self):
        return conf15		
    def getconf16(self):
        return conf16		
    def getconf17(self):
        return conf17		
    def getconf18(self):
        return conf18		
    def getconf19(self):
        return conf19		
    def getconf20(self):
        return conf20		
    def getconf21(self):
        return conf21		
    def getconf22(self):
        return conf22		
    def getconf23(self):
        return conf23		
    def getconf24(self):
        return conf24		
    def getconf25(self):
        return conf25		
    def getconf26(self):
        return conf26		
    def getconf27(self):
        return conf27		
    def getconf28(self):
        return conf28		
    def getconf29(self):
        return conf29		
    def getconf30(self):
        return conf30		
    def getconf31(self):
        return conf31		
    def getconf32(self):
        return conf32		
    def getconf33(self):
        return conf33		
    def getconf34(self):
        return conf34		
    def getconf35(self):
        return conf35		
    def getconf36(self):
        return conf36		
    def getconf37(self):
        return conf37		
    def getconf38(self):
        return conf38		
    def getconf39(self):
        return conf39		
    def getconf40(self):
        return conf40		
    def getconf41(self):
        return conf41		
    def getconf42(self):
        return conf42		
    def getconf43(self):
        return conf43		
    def getconf44(self):
        return conf44		
    def getconf45(self):
        return conf45		
    def getconf46(self):
        return conf46		
    def getconf47(self):
        return conf47		
    def getconf48(self):
        return conf48		
    def getconf49(self):
        return conf49		
    def getconf50(self):
        return conf50		
    def getconf51(self):
        return conf51		
    def getconf52(self):
        return conf52		
    def getconf53(self):
        return conf53		
    def getconf54(self):
        return conf54		
    def getconf55(self):
        return conf55		
    def getconf56(self):
        return conf56		
    def getconf57(self):
        return conf57		
    def getconf58(self):
        return conf58		
    def getconf59(self):
        return conf59		
    def getconf60(self):
        return conf60		
    def getconf61(self):
        return conf61		
    def getconf62(self):
        return conf62		
    def getconf63(self):
        return conf63		
    def getconf64(self):
        return conf64		
    def getconf65(self):
        return conf65		
    def getconf66(self):
        return conf66		
    def getconf67(self):
        return conf67		
    def getconf68(self):
        return conf68		
    def getconf69(self):
        return conf69		
    def getconf70(self):
        return conf70		
    def getconf71(self):
        return conf71		
    def getconf72(self):
        return conf72		
    def getconf73(self):
        return conf73		
    def getconf74(self):
        return conf74		
    def getconf75(self):
        return conf75		
    def getconf76(self):
        return conf76		
    def getconf77(self):
        return conf77		
    def getconf78(self):
        return conf78		
    def getconf79(self):
        return conf79		
    def getconf80(self):
        return conf80		
    def getconf81(self):
        return conf81		
    def getconf82(self):
        return conf82		
    def getconf83(self):
        return conf83		
    def getconf84(self):
        return conf84		
    def getconf85(self):
        return conf85		
    def getconf86(self):
        return conf86		
    def getconf87(self):
        return conf87		
    def getconf88(self):
        return conf88		
    def getconf89(self):
        return conf89		
    def getconf90(self):
        return conf90		
    def getconf91(self):
        return conf91		
    def getconf92(self):
        return conf92		
    def getconf93(self):
        return conf93		
    def getconf94(self):
        return conf94		
    def getconf95(self):
        return conf95		
    def getconf96(self):
        return conf96		
    def getconf97(self):
        return conf97		
    def getconf98(self):
        return conf98		
    def getconf99(self):
        return conf99		
    def getconf100(self):
        return conf100		
    def getconf101(self):
        return conf101		
    def getconf102(self):
        return conf102		
    def getconf103(self):
        return conf103		
    def getconf104(self):
        return conf104		
    def getconf105(self):
        return conf105		
    def getconf106(self):
        return conf106		
    def getconf107(self):
        return conf107		
    def getconf108(self):
        return conf108		
    def getconf109(self):
        return conf109		
    def getconf110(self):
        return conf110		
    def getconf111(self):
        return conf111		
    def getconf112(self):
        return conf112		
    def getconf113(self):
        return conf113		
    def getconf114(self):
        return conf114		
    def getconf115(self):
        return conf115		
    def getconf116(self):
        return conf116		
    def getconf117(self):
        return conf117		
    def getconf118(self):
        return conf118		
    def getconf119(self):
        return conf119		
    def getconf120(self):
        return conf120		
    def getconf121(self):
        return conf121		
    def getconf122(self):
        return conf122		
    def getconf123(self):
        return conf123		
    def getconf124(self):
        return conf124		
    def getconf125(self):
        return conf125		
    def getconf126(self):
        return conf126		
    def getconf127(self):
        return conf127		
    def getconf128(self):
        return conf128		
    def getconf129(self):
        return conf129		
    def getconf130(self):
        return conf130		
    def getconf131(self):
        return conf131		
    def getconf132(self):
        return conf132		
    def getconf133(self):
        return conf133		
    def getconf134(self):
        return conf134		
    def getconf135(self):
        return conf135		
    def getconf136(self):
        return conf136		
    def getconf137(self):
        return conf137		
    def getconf138(self):
        return conf138		
    def getconf139(self):
        return conf139		
    def getconf140(self):
        return conf140		
    def getconf141(self):
        return conf141		
    def getconf142(self):
        return conf142		
    def getconf143(self):
        return conf143		
    def getconf144(self):
        return conf144		
    def getconf145(self):
        return conf145		
    def getconf146(self):
        return conf146		
    def getconf147(self):
        return conf147		
    def getconf148(self):
        return conf148		
    def getconf149(self):
        return conf149		
    def getconf150(self):
        return conf150		
    def getconf151(self):
        return conf151		
    def getconf152(self):
        return conf152		
    def getconf153(self):
        return conf153		
    def getconf154(self):
        return conf154		
    def getconf155(self):
        return conf155		
    def getconf156(self):
        return conf156		
    def getconf157(self):
        return conf157		
    def getconf158(self):
        return conf158		
    def getconf159(self):
        return conf159		
    def getconf160(self):
        return conf160		
    def getconf161(self):
        return conf161		
    def getconf162(self):
        return conf162		
    def getconf163(self):
        return conf163		
    def getconf164(self):
        return conf164		
    def getconf165(self):
        return conf165		
    def getconf166(self):
        return conf166		
    def getconf167(self):
        return conf167		
    def getconf168(self):
        return conf168		
    def getconf169(self):
        return conf169		
    def getconf170(self):
        return conf170		
    def getconf171(self):
        return conf171		
    def getconf172(self):
        return conf172		
    def getconf173(self):
        return conf173		
    def getconf174(self):
        return conf174		
    def getconf175(self):
        return conf175		
    def getconf176(self):
        return conf176		
    def getconf177(self):
        return conf177		
    def getconf178(self):
        return conf178		
    def getconf179(self):
        return conf179		
    def getconf180(self):
        return conf180		
    def getconf181(self):
        return conf181		
    def getconf182(self):
        return conf182		
    def getconf183(self):
        return conf183		
    def getconf184(self):
        return conf184		
    def getconf185(self):
        return conf185		
    def getconf186(self):
        return conf186		
    def getconf187(self):
        return conf187		
    def getconf188(self):
        return conf188		
    def getconf189(self):
        return conf189		
    def getconf190(self):
        return conf190		
    def getconf191(self):
        return conf191		
    def getconf192(self):
        return conf192		
    def getconf193(self):
        return conf193		
    def getconf194(self):
        return conf194		
    def getconf195(self):
        return conf195		
    def getconf196(self):
        return conf196		
    def getconf197(self):
        return conf197		
    def getconf198(self):
        return conf198		
    def getconf199(self):
        return conf199		
    def getconf200(self):
        return conf200		
    def getconf201(self):
        return conf201		
    def getconf202(self):
        return conf202		
    def getconf203(self):
        return conf203		
    def getconf204(self):
        return conf204		
    def getconf205(self):
        return conf205		
    def getconf206(self):
        return conf206		
    def getconf207(self):
        return conf207		
    def getconf208(self):
        return conf208		
    def getconf209(self):
        return conf209		
    def getconf210(self):
        return conf210		
    def getconf211(self):
        return conf211		
    def getconf212(self):
        return conf212		
    def getconf213(self):
        return conf213		
    def getconf214(self):
        return conf214		
    def getconf215(self):
        return conf215		
    def getconf216(self):
        return conf216		
    def getconf217(self):
        return conf217		
    def getconf218(self):
        return conf218		
    def getconf219(self):
        return conf219		
    def getconf220(self):
        return conf220		
    def getconf221(self):
        return conf221		
    def getconf222(self):
        return conf222		
    def getconf223(self):
        return conf223		
    def getconf224(self):
        return conf224		
    def getconf225(self):
        return conf225		
    def getconf226(self):
        return conf226		
    def getconf227(self):
        return conf227		
    def getconf228(self):
        return conf228		
    def getconf229(self):
        return conf229		
    def getconf230(self):
        return conf230		
    def getconf231(self):
        return conf231		
    def getconf232(self):
        return conf232		
    def getconf233(self):
        return conf233		
    def getconf234(self):
        return conf234		
    def getconf235(self):
        return conf235		
    def getconf236(self):
        return conf236		
    def getconf237(self):
        return conf237		
    def getconf238(self):
        return conf238		
    def getconf239(self):
        return conf239		
    def getconf240(self):
        return conf240		
    def getconf241(self):
        return conf241		
    def getconf242(self):
        return conf242		
    def getconf243(self):
        return conf243		
    def getconf244(self):
        return conf244		
    def getconf245(self):
        return conf245		
    def getconf246(self):
        return conf246		
    def getconf247(self):
        return conf247		
    def getconf248(self):
        return conf248		
    def getconf249(self):
        return conf249		
    def getconf250(self):
        return conf250		
    def getconf251(self):
        return conf251		
    def getconf252(self):
        return conf252		
    def getconf253(self):
        return conf253		
    def getconf254(self):
        return conf254		
    def getconf255(self):
        return conf255		
    def getconf256(self):
        return conf256		
    def getconf257(self):
        return conf257		
    def getconf258(self):
        return conf258		
    def getconf259(self):
        return conf259		
    def getconf260(self):
        return conf260		
    def getconf261(self):
        return conf261		
    def getconf262(self):
        return conf262		
    def getconf263(self):
        return conf263		
    def getconf264(self):
        return conf264		
    def getconf265(self):
        return conf265		
    def getconf266(self):
        return conf266		
    def getconf267(self):
        return conf267		
    def getconf268(self):
        return conf268		
    def getconf269(self):
        return conf269		
    def getconf270(self):
        return conf270		
    def getconf271(self):
        return conf271		
    def getconf272(self):
        return conf272		
    def getconf273(self):
        return conf273		
    def getconf274(self):
        return conf274		
    def getconf275(self):
        return conf275		
    def getconf276(self):
        return conf276		
    def getconf277(self):
        return conf277		
    def getconf278(self):
        return conf278		
    def getconf279(self):
        return conf279		
    def getconf280(self):
        return conf280		
    def getconf281(self):
        return conf281		
    def getconf282(self):
        return conf282		
    def getconf283(self):
        return conf283		
    def getconf284(self):
        return conf284		
    def getconf285(self):
        return conf285		
    def getconf286(self):
        return conf286		
    def getconf287(self):
        return conf287		
    def getconf288(self):
        return conf288		
    def getconf289(self):
        return conf289		
    def getconf290(self):
        return conf290		
    def getconf291(self):
        return conf291		
    def getconf292(self):
        return conf292		
    def getconf293(self):
        return conf293		
    def getconf294(self):
        return conf294		
    def getconf295(self):
        return conf295		
    def getconf296(self):
        return conf296		
    def getconf297(self):
        return conf297		
    def getconf298(self):
        return conf298		
    def getconf299(self):
        return conf299		
    def getconf300(self):
        return conf300		
    def getconf301(self):
        return conf301		
    def getconf302(self):
        return conf302		
    def getconf303(self):
        return conf303		
    def getconf304(self):
        return conf304		
    def getconf305(self):
        return conf305		
    def getconf306(self):
        return conf306		
    def getconf307(self):
        return conf307		
    def getconf308(self):
        return conf308		
    def getconf309(self):
        return conf309		
    def getconf310(self):
        return conf310		
    def getconf311(self):
        return conf311		
    def getconf312(self):
        return conf312		
    def getconf313(self):
        return conf313		
    def getconf314(self):
        return conf314		
    def getconf315(self):
        return conf315		
    def getconf316(self):
        return conf316		
    def getconf317(self):
        return conf317		
    def getconf318(self):
        return conf318		
    def getconf319(self):
        return conf319		
    def getconf320(self):
        return conf320		
    def getconf321(self):
        return conf321		
    def getconf322(self):
        return conf322		
    def getconf323(self):
        return conf323		
    def getconf324(self):
        return conf324		
    def getconf325(self):
        return conf325		
    def getconf326(self):
        return conf326		
    def getconf327(self):
        return conf327		
    def getconf328(self):
        return conf328		
    def getconf329(self):
        return conf329		
    def getconf330(self):
        return conf330		
    def getconf331(self):
        return conf331		
    def getconf332(self):
        return conf332		
    def getconf333(self):
        return conf333		
    def getconf334(self):
        return conf334		
    def getconf335(self):
        return conf335		
    def getconf336(self):
        return conf336		
    def getconf337(self):
        return conf337		
    def getconf338(self):
        return conf338		
    def getconf339(self):
        return conf339		
    def getconf340(self):
        return conf340		
    def getconf341(self):
        return conf341		
    def getconf342(self):
        return conf342		
    def getconf343(self):
        return conf343		
    def getconf344(self):
        return conf344		
    def getconf345(self):
        return conf345		
    def getconf346(self):
        return conf346		
    def getconf347(self):
        return conf347		
    def getconf348(self):
        return conf348		
    def getconf349(self):
        return conf349		
    def getconf350(self):
        return conf350		
    def getconf351(self):
        return conf351		
    def getconf352(self):
        return conf352		
    def getconf353(self):
        return conf353		
    def getconf354(self):
        return conf354		
    def getconf355(self):
        return conf355
    def getconf356(self):
        return conf356
    def getconf356(self):
        return conf357
    def getconf356(self):
        return conf358
    def getconf356(self):
        return conf359
    def getconf356(self):
        return conf360
    def setconf1(self, id, value):
        conf1[id]=value
    def setconf2(self, id, value):
        conf2[id]=value
    def setconf3(self, id, value):
        conf3[id]=value
    def setconf4(self, id, value):
        conf4[id]=value
    def setconf5(self, id, value):
        conf5[id]=value
    def setconf6(self, id, value):
        conf6[id]=value
    def setconf7(self, id, value):
        conf7[id]=value
    def setconf8(self, id, value):
        conf8[id]=value
    def setconf9(self, id, value):
        conf9[id]=value
    def setconf10(self, id, value):
        conf10[id]=value
    def setconf11(self, id, value):
        conf11[id]=value
    def setconf12(self, id, value):
        conf12[id]=value
    def setconf13(self, id, value):
        conf13[id]=value
    def setconf14(self, id, value):
        conf14[id]=value
    def setconf15(self, id, value):
        conf15[id]=value
    def setconf16(self, id, value):
        conf16[id]=value
    def setconf17(self, id, value):
        conf17[id]=value
    def setconf18(self, id, value):
        conf18[id]=value
    def setconf19(self, id, value):
        conf19[id]=value
    def setconf20(self, id, value):
        conf20[id]=value
    def setconf21(self, id, value):
        conf21[id]=value
    def setconf22(self, id, value):
        conf22[id]=value
    def setconf23(self, id, value):
        conf23[id]=value
    def setconf24(self, id, value):
        conf24[id]=value
    def setconf25(self, id, value):
        conf25[id]=value
    def setconf26(self, id, value):
        conf26[id]=value
    def setconf27(self, id, value):
        conf27[id]=value
    def setconf28(self, id, value):
        conf28[id]=value
    def setconf29(self, id, value):
        conf29[id]=value
    def setconf30(self, id, value):
        conf30[id]=value
    def setconf31(self, id, value):
        conf31[id]=value
    def setconf32(self, id, value):
        conf32[id]=value
    def setconf33(self, id, value):
        conf33[id]=value
    def setconf34(self, id, value):
        conf34[id]=value
    def setconf35(self, id, value):
        conf35[id]=value
    def setconf36(self, id, value):
        conf36[id]=value
    def setconf37(self, id, value):
        conf37[id]=value
    def setconf38(self, id, value):
        conf38[id]=value
    def setconf39(self, id, value):
        conf39[id]=value
    def setconf40(self, id, value):
        conf40[id]=value
    def setconf41(self, id, value):
        conf41[id]=value
    def setconf42(self, id, value):
        conf42[id]=value
    def setconf43(self, id, value):
        conf43[id]=value
    def setconf44(self, id, value):
        conf44[id]=value
    def setconf45(self, id, value):
        conf45[id]=value
    def setconf46(self, id, value):
        conf46[id]=value
    def setconf47(self, id, value):
        conf47[id]=value
    def setconf48(self, id, value):
        conf48[id]=value
    def setconf49(self, id, value):
        conf49[id]=value
    def setconf50(self, id, value):
        conf50[id]=value
    def setconf51(self, id, value):
        conf51[id]=value
    def setconf52(self, id, value):
        conf52[id]=value
    def setconf53(self, id, value):
        conf53[id]=value
    def setconf54(self, id, value):
        conf54[id]=value
    def setconf55(self, id, value):
        conf55[id]=value
    def setconf56(self, id, value):
        conf56[id]=value
    def setconf57(self, id, value):
        conf57[id]=value
    def setconf58(self, id, value):
        conf58[id]=value
    def setconf59(self, id, value):
        conf59[id]=value
    def setconf60(self, id, value):
        conf60[id]=value
    def setconf61(self, id, value):
        conf61[id]=value
    def setconf62(self, id, value):
        conf62[id]=value
    def setconf63(self, id, value):
        conf63[id]=value
    def setconf64(self, id, value):
        conf64[id]=value
    def setconf65(self, id, value):
        conf65[id]=value
    def setconf66(self, id, value):
        conf66[id]=value
    def setconf67(self, id, value):
        conf67[id]=value
    def setconf68(self, id, value):
        conf68[id]=value
    def setconf69(self, id, value):
        conf69[id]=value
    def setconf70(self, id, value):
        conf70[id]=value
    def setconf71(self, id, value):
        conf71[id]=value
    def setconf72(self, id, value):
        conf72[id]=value
    def setconf73(self, id, value):
        conf73[id]=value
    def setconf74(self, id, value):
        conf74[id]=value
    def setconf75(self, id, value):
        conf75[id]=value
    def setconf76(self, id, value):
        conf76[id]=value
    def setconf77(self, id, value):
        conf77[id]=value
    def setconf78(self, id, value):
        conf78[id]=value
    def setconf79(self, id, value):
        conf79[id]=value
    def setconf80(self, id, value):
        conf80[id]=value
    def setconf81(self, id, value):
        conf81[id]=value
    def setconf82(self, id, value):
        conf82[id]=value
    def setconf83(self, id, value):
        conf83[id]=value
    def setconf84(self, id, value):
        conf84[id]=value
    def setconf85(self, id, value):
        conf85[id]=value
    def setconf86(self, id, value):
        conf86[id]=value
    def setconf87(self, id, value):
        conf87[id]=value
    def setconf88(self, id, value):
        conf88[id]=value
    def setconf89(self, id, value):
        conf89[id]=value
    def setconf90(self, id, value):
        conf90[id]=value
    def setconf91(self, id, value):
        conf91[id]=value
    def setconf92(self, id, value):
        conf92[id]=value
    def setconf93(self, id, value):
        conf93[id]=value
    def setconf94(self, id, value):
        conf94[id]=value
    def setconf95(self, id, value):
        conf95[id]=value
    def setconf96(self, id, value):
        conf96[id]=value
    def setconf97(self, id, value):
        conf97[id]=value
    def setconf98(self, id, value):
        conf98[id]=value
    def setconf99(self, id, value):
        conf99[id]=value
    def setconf100(self, id, value):
        conf100[id]=value
    def setconf101(self, id, value):
        conf101[id]=value
    def setconf102(self, id, value):
        conf102[id]=value
    def setconf103(self, id, value):
        conf103[id]=value
    def setconf104(self, id, value):
        conf104[id]=value
    def setconf105(self, id, value):
        conf105[id]=value
    def setconf106(self, id, value):
        conf106[id]=value
    def setconf107(self, id, value):
        conf107[id]=value
    def setconf108(self, id, value):
        conf108[id]=value
    def setconf109(self, id, value):
        conf109[id]=value
    def setconf110(self, id, value):
        conf110[id]=value
    def setconf111(self, id, value):
        conf111[id]=value
    def setconf112(self, id, value):
        conf112[id]=value
    def setconf113(self, id, value):
        conf113[id]=value
    def setconf114(self, id, value):
        conf114[id]=value
    def setconf115(self, id, value):
        conf115[id]=value
    def setconf116(self, id, value):
        conf116[id]=value
    def setconf117(self, id, value):
        conf117[id]=value
    def setconf118(self, id, value):
        conf118[id]=value
    def setconf119(self, id, value):
        conf119[id]=value
    def setconf120(self, id, value):
        conf120[id]=value
    def setconf121(self, id, value):
        conf121[id]=value
    def setconf122(self, id, value):
        conf122[id]=value
    def setconf123(self, id, value):
        conf123[id]=value
    def setconf124(self, id, value):
        conf124[id]=value
    def setconf125(self, id, value):
        conf125[id]=value
    def setconf126(self, id, value):
        conf126[id]=value
    def setconf127(self, id, value):
        conf127[id]=value
    def setconf128(self, id, value):
        conf128[id]=value
    def setconf129(self, id, value):
        conf129[id]=value
    def setconf130(self, id, value):
        conf130[id]=value
    def setconf131(self, id, value):
        conf131[id]=value
    def setconf132(self, id, value):
        conf132[id]=value
    def setconf133(self, id, value):
        conf133[id]=value
    def setconf134(self, id, value):
        conf134[id]=value
    def setconf135(self, id, value):
        conf135[id]=value
    def setconf136(self, id, value):
        conf136[id]=value
    def setconf137(self, id, value):
        conf137[id]=value
    def setconf138(self, id, value):
        conf138[id]=value
    def setconf139(self, id, value):
        conf139[id]=value
    def setconf140(self, id, value):
        conf140[id]=value
    def setconf141(self, id, value):
        conf141[id]=value
    def setconf142(self, id, value):
        conf142[id]=value
    def setconf143(self, id, value):
        conf143[id]=value
    def setconf144(self, id, value):
        conf144[id]=value
    def setconf145(self, id, value):
        conf145[id]=value
    def setconf146(self, id, value):
        conf146[id]=value
    def setconf147(self, id, value):
        conf147[id]=value
    def setconf148(self, id, value):
        conf148[id]=value
    def setconf149(self, id, value):
        conf149[id]=value
    def setconf150(self, id, value):
        conf150[id]=value
    def setconf151(self, id, value):
        conf151[id]=value
    def setconf152(self, id, value):
        conf152[id]=value
    def setconf153(self, id, value):
        conf153[id]=value
    def setconf154(self, id, value):
        conf154[id]=value
    def setconf155(self, id, value):
        conf155[id]=value
    def setconf156(self, id, value):
        conf156[id]=value
    def setconf157(self, id, value):
        conf157[id]=value
    def setconf158(self, id, value):
        conf158[id]=value
    def setconf159(self, id, value):
        conf159[id]=value
    def setconf160(self, id, value):
        conf160[id]=value
    def setconf161(self, id, value):
        conf161[id]=value
    def setconf162(self, id, value):
        conf162[id]=value
    def setconf163(self, id, value):
        conf163[id]=value
    def setconf164(self, id, value):
        conf164[id]=value
    def setconf165(self, id, value):
        conf165[id]=value
    def setconf166(self, id, value):
        conf166[id]=value
    def setconf167(self, id, value):
        conf167[id]=value
    def setconf168(self, id, value):
        conf168[id]=value
    def setconf169(self, id, value):
        conf169[id]=value
    def setconf170(self, id, value):
        conf170[id]=value
    def setconf171(self, id, value):
        conf171[id]=value
    def setconf172(self, id, value):
        conf172[id]=value
    def setconf173(self, id, value):
        conf173[id]=value
    def setconf174(self, id, value):
        conf174[id]=value
    def setconf175(self, id, value):
        conf175[id]=value
    def setconf176(self, id, value):
        conf176[id]=value
    def setconf177(self, id, value):
        conf177[id]=value
    def setconf178(self, id, value):
        conf178[id]=value
    def setconf179(self, id, value):
        conf179[id]=value
    def setconf180(self, id, value):
        conf180[id]=value
    def setconf181(self, id, value):
        conf181[id]=value
    def setconf182(self, id, value):
        conf182[id]=value
    def setconf183(self, id, value):
        conf183[id]=value
    def setconf184(self, id, value):
        conf184[id]=value
    def setconf185(self, id, value):
        conf185[id]=value
    def setconf186(self, id, value):
        conf186[id]=value
    def setconf187(self, id, value):
        conf187[id]=value
    def setconf188(self, id, value):
        conf188[id]=value
    def setconf189(self, id, value):
        conf189[id]=value
    def setconf190(self, id, value):
        conf190[id]=value
    def setconf191(self, id, value):
        conf191[id]=value
    def setconf192(self, id, value):
        conf192[id]=value
    def setconf193(self, id, value):
        conf193[id]=value
    def setconf194(self, id, value):
        conf194[id]=value
    def setconf195(self, id, value):
        conf195[id]=value
    def setconf196(self, id, value):
        conf196[id]=value
    def setconf197(self, id, value):
        conf197[id]=value
    def setconf198(self, id, value):
        conf198[id]=value
    def setconf199(self, id, value):
        conf199[id]=value
    def setconf200(self, id, value):
        conf200[id]=value
    def setconf201(self, id, value):
        conf201[id]=value
    def setconf202(self, id, value):
        conf202[id]=value
    def setconf203(self, id, value):
        conf203[id]=value
    def setconf204(self, id, value):
        conf204[id]=value
    def setconf205(self, id, value):
        conf205[id]=value
    def setconf206(self, id, value):
        conf206[id]=value
    def setconf207(self, id, value):
        conf207[id]=value
    def setconf208(self, id, value):
        conf208[id]=value
    def setconf209(self, id, value):
        conf209[id]=value
    def setconf210(self, id, value):
        conf210[id]=value
    def setconf211(self, id, value):
        conf211[id]=value
    def setconf212(self, id, value):
        conf212[id]=value
    def setconf213(self, id, value):
        conf213[id]=value
    def setconf214(self, id, value):
        conf214[id]=value
    def setconf215(self, id, value):
        conf215[id]=value
    def setconf216(self, id, value):
        conf216[id]=value
    def setconf217(self, id, value):
        conf217[id]=value
    def setconf218(self, id, value):
        conf218[id]=value
    def setconf219(self, id, value):
        conf219[id]=value
    def setconf220(self, id, value):
        conf220[id]=value
    def setconf221(self, id, value):
        conf221[id]=value
    def setconf222(self, id, value):
        conf222[id]=value
    def setconf223(self, id, value):
        conf223[id]=value
    def setconf224(self, id, value):
        conf224[id]=value
    def setconf225(self, id, value):
        conf225[id]=value
    def setconf226(self, id, value):
        conf226[id]=value
    def setconf227(self, id, value):
        conf227[id]=value
    def setconf228(self, id, value):
        conf228[id]=value
    def setconf229(self, id, value):
        conf229[id]=value
    def setconf230(self, id, value):
        conf230[id]=value
    def setconf231(self, id, value):
        conf231[id]=value
    def setconf232(self, id, value):
        conf232[id]=value
    def setconf233(self, id, value):
        conf233[id]=value
    def setconf234(self, id, value):
        conf234[id]=value
    def setconf235(self, id, value):
        conf235[id]=value
    def setconf236(self, id, value):
        conf236[id]=value
    def setconf237(self, id, value):
        conf237[id]=value
    def setconf238(self, id, value):
        conf238[id]=value
    def setconf239(self, id, value):
        conf239[id]=value
    def setconf240(self, id, value):
        conf240[id]=value
    def setconf241(self, id, value):
        conf241[id]=value
    def setconf242(self, id, value):
        conf242[id]=value
    def setconf243(self, id, value):
        conf243[id]=value
    def setconf244(self, id, value):
        conf244[id]=value
    def setconf245(self, id, value):
        conf245[id]=value
    def setconf246(self, id, value):
        conf246[id]=value
    def setconf247(self, id, value):
        conf247[id]=value
    def setconf248(self, id, value):
        conf248[id]=value
    def setconf249(self, id, value):
        conf249[id]=value
    def setconf250(self, id, value):
        conf250[id]=value
    def setconf251(self, id, value):
        conf251[id]=value
    def setconf252(self, id, value):
        conf252[id]=value
    def setconf253(self, id, value):
        conf253[id]=value
    def setconf254(self, id, value):
        conf254[id]=value
    def setconf255(self, id, value):
        conf255[id]=value
    def setconf256(self, id, value):
        conf256[id]=value
    def setconf257(self, id, value):
        conf257[id]=value
    def setconf258(self, id, value):
        conf258[id]=value
    def setconf259(self, id, value):
        conf259[id]=value
    def setconf260(self, id, value):
        conf260[id]=value
    def setconf261(self, id, value):
        conf261[id]=value
    def setconf262(self, id, value):
        conf262[id]=value
    def setconf263(self, id, value):
        conf263[id]=value
    def setconf264(self, id, value):
        conf264[id]=value
    def setconf265(self, id, value):
        conf265[id]=value
    def setconf266(self, id, value):
        conf266[id]=value
    def setconf267(self, id, value):
        conf267[id]=value
    def setconf268(self, id, value):
        conf268[id]=value
    def setconf269(self, id, value):
        conf269[id]=value
    def setconf270(self, id, value):
        conf270[id]=value
    def setconf271(self, id, value):
        conf271[id]=value
    def setconf272(self, id, value):
        conf272[id]=value
    def setconf273(self, id, value):
        conf273[id]=value
    def setconf274(self, id, value):
        conf274[id]=value
    def setconf275(self, id, value):
        conf275[id]=value
    def setconf276(self, id, value):
        conf276[id]=value
    def setconf277(self, id, value):
        conf277[id]=value
    def setconf278(self, id, value):
        conf278[id]=value
    def setconf279(self, id, value):
        conf279[id]=value
    def setconf280(self, id, value):
        conf280[id]=value
    def setconf281(self, id, value):
        conf281[id]=value
    def setconf282(self, id, value):
        conf282[id]=value
    def setconf283(self, id, value):
        conf283[id]=value
    def setconf284(self, id, value):
        conf284[id]=value
    def setconf285(self, id, value):
        conf285[id]=value
    def setconf286(self, id, value):
        conf286[id]=value
    def setconf287(self, id, value):
        conf287[id]=value
    def setconf288(self, id, value):
        conf288[id]=value
    def setconf289(self, id, value):
        conf289[id]=value
    def setconf290(self, id, value):
        conf290[id]=value
    def setconf291(self, id, value):
        conf291[id]=value
    def setconf292(self, id, value):
        conf292[id]=value
    def setconf293(self, id, value):
        conf293[id]=value
    def setconf294(self, id, value):
        conf294[id]=value
    def setconf295(self, id, value):
        conf295[id]=value
    def setconf296(self, id, value):
        conf296[id]=value
    def setconf297(self, id, value):
        conf297[id]=value
    def setconf298(self, id, value):
        conf298[id]=value
    def setconf299(self, id, value):
        conf299[id]=value
    def setconf300(self, id, value):
        conf300[id]=value
    def setconf301(self, id, value):
        conf301[id]=value
    def setconf302(self, id, value):
        conf302[id]=value
    def setconf303(self, id, value):
        conf303[id]=value
    def setconf304(self, id, value):
        conf304[id]=value
    def setconf305(self, id, value):
        conf305[id]=value
    def setconf306(self, id, value):
        conf306[id]=value
    def setconf307(self, id, value):
        conf307[id]=value
    def setconf308(self, id, value):
        conf308[id]=value
    def setconf309(self, id, value):
        conf309[id]=value
    def setconf310(self, id, value):
        conf310[id]=value
    def setconf311(self, id, value):
        conf311[id]=value
    def setconf312(self, id, value):
        conf312[id]=value
    def setconf313(self, id, value):
        conf313[id]=value
    def setconf314(self, id, value):
        conf314[id]=value
    def setconf315(self, id, value):
        conf315[id]=value
    def setconf316(self, id, value):
        conf316[id]=value
    def setconf317(self, id, value):
        conf317[id]=value
    def setconf318(self, id, value):
        conf318[id]=value
    def setconf319(self, id, value):
        conf319[id]=value
    def setconf320(self, id, value):
        conf320[id]=value
    def setconf321(self, id, value):
        conf321[id]=value
    def setconf322(self, id, value):
        conf322[id]=value
    def setconf323(self, id, value):
        conf323[id]=value
    def setconf324(self, id, value):
        conf324[id]=value
    def setconf325(self, id, value):
        conf325[id]=value
    def setconf326(self, id, value):
        conf326[id]=value
    def setconf327(self, id, value):
        conf327[id]=value
    def setconf328(self, id, value):
        conf328[id]=value
    def setconf329(self, id, value):
        conf329[id]=value
    def setconf330(self, id, value):
        conf330[id]=value
    def setconf331(self, id, value):
        conf331[id]=value
    def setconf332(self, id, value):
        conf332[id]=value
    def setconf333(self, id, value):
        conf333[id]=value
    def setconf334(self, id, value):
        conf334[id]=value
    def setconf335(self, id, value):
        conf335[id]=value
    def setconf336(self, id, value):
        conf336[id]=value
    def setconf337(self, id, value):
        conf337[id]=value
    def setconf338(self, id, value):
        conf338[id]=value
    def setconf339(self, id, value):
        conf339[id]=value
    def setconf340(self, id, value):
        conf340[id]=value
    def setconf341(self, id, value):
        conf341[id]=value
    def setconf342(self, id, value):
        conf342[id]=value
    def setconf343(self, id, value):
        conf343[id]=value
    def setconf344(self, id, value):
        conf344[id]=value
    def setconf345(self, id, value):
        conf345[id]=value
    def setconf346(self, id, value):
        conf346[id]=value
    def setconf347(self, id, value):
        conf347[id]=value
    def setconf348(self, id, value):
        conf348[id]=value
    def setconf349(self, id, value):
        conf349[id]=value
    def setconf350(self, id, value):
        conf350[id]=value
    def setconf351(self, id, value):
        conf351[id]=value
    def setconf352(self, id, value):
        conf352[id]=value
    def setconf353(self, id, value):
        conf353[id]=value
    def setconf354(self, id, value):
        conf354[id]=value
    def setconf355(self, id, value):
        conf355[id]=value
    def setconf356(self, id, value):
        conf356[id]=value
    def setconf357(self, id, value):
        conf353[id]=value
    def setconf358(self, id, value):
        conf354[id]=value
    def setconf359(self, id, value):
        conf355[id]=value
    def setconf360(self, id, value):
        conf356[id]=value
    def createFile(self,file):
        if exists(file):
            os.chmod(file,stat.S_IWRITE )
        fp = open(file, 'w')
        fp.write(conf1[0]+" \""+conf1[1]+"\" \""+conf1[2]+"\" \""+conf1[3]+"\"\n")
        fp.write(conf2[0]+" \""+conf2[1]+"\" \""+conf2[2]+"\" \""+conf2[3]+"\"\n")
        fp.write(conf3[0]+" \""+conf3[1]+"\" \""+conf3[2]+"\" \""+conf3[3]+"\"\n")
        fp.write(conf4[0]+" \""+conf4[1]+"\" \""+conf4[2]+"\" \""+conf4[3]+"\"\n")
        fp.write(conf5[0]+" \""+conf5[1]+"\" \""+conf5[2]+"\" \""+conf5[3]+"\"\n")
        fp.write(conf6[0]+" \""+conf6[1]+"\" \""+conf6[2]+"\" \""+conf6[3]+"\"\n")
        fp.write(conf7[0]+" \""+conf7[1]+"\" \""+conf7[2]+"\" \""+conf7[3]+"\"\n")
        fp.write(conf8[0]+" \""+conf8[1]+"\" \""+conf8[2]+"\" \""+conf8[3]+"\"\n")
        fp.write(conf9[0]+" \""+conf9[1]+"\" \""+conf9[2]+"\" \""+conf9[3]+"\"\n")
        fp.write(conf10[0]+" \""+conf10[1]+"\" \""+conf10[2]+"\" \""+conf10[3]+"\"\n")
        fp.write(conf11[0]+" \""+conf11[1]+"\" \""+conf11[2]+"\" \""+conf11[3]+"\"\n")
        fp.write(conf12[0]+" \""+conf12[1]+"\" \""+conf12[2]+"\" \""+conf12[3]+"\"\n")
        fp.write(conf13[0]+" \""+conf13[1]+"\" \""+conf13[2]+"\" \""+conf13[3]+"\"\n")
        fp.write(conf14[0]+" \""+conf14[1]+"\" \""+conf14[2]+"\" \""+conf14[3]+"\"\n")
        fp.write(conf15[0]+" \""+conf15[1]+"\" \""+conf15[2]+"\" \""+conf15[3]+"\"\n")
        fp.write(conf16[0]+" \""+conf16[1]+"\" \""+conf16[2]+"\" \""+conf16[3]+"\"\n")
        fp.write(conf17[0]+" \""+conf17[1]+"\" \""+conf17[2]+"\" \""+conf17[3]+"\"\n")
        fp.write(conf18[0]+" \""+conf18[1]+"\" \""+conf18[2]+"\" \""+conf18[3]+"\"\n")
        fp.write(conf19[0]+" \""+conf19[1]+"\" \""+conf19[2]+"\" \""+conf19[3]+"\"\n")
        fp.write(conf20[0]+" \""+conf20[1]+"\" \""+conf20[2]+"\" \""+conf20[3]+"\"\n")
        fp.write(conf21[0]+" \""+conf21[1]+"\" \""+conf21[2]+"\" \""+conf21[3]+"\"\n")
        fp.write(conf22[0]+" \""+conf22[1]+"\" \""+conf22[2]+"\" \""+conf22[3]+"\"\n")
        fp.write(conf23[0]+" \""+conf23[1]+"\" \""+conf23[2]+"\" \""+conf23[3]+"\"\n")
        fp.write(conf24[0]+" \""+conf24[1]+"\" \""+conf24[2]+"\" \""+conf24[3]+"\"\n")
        fp.write(conf25[0]+" \""+conf25[1]+"\" \""+conf25[2]+"\" \""+conf25[3]+"\"\n")
        fp.write(conf26[0]+" \""+conf26[1]+"\" \""+conf26[2]+"\" \""+conf26[3]+"\"\n")
        fp.write(conf27[0]+" \""+conf27[1]+"\" \""+conf27[2]+"\" \""+conf27[3]+"\"\n")
        fp.write(conf28[0]+" \""+conf28[1]+"\" \""+conf28[2]+"\" \""+conf28[3]+"\"\n")
        fp.write(conf29[0]+" \""+conf29[1]+"\" \""+conf29[2]+"\" \""+conf29[3]+"\"\n")
        fp.write(conf30[0]+" \""+conf30[1]+"\" \""+conf30[2]+"\" \""+conf30[3]+"\"\n")
        fp.write(conf31[0]+" \""+conf31[1]+"\" \""+conf31[2]+"\" \""+conf31[3]+"\"\n")
        fp.write(conf32[0]+" \""+conf32[1]+"\" \""+conf32[2]+"\" \""+conf32[3]+"\"\n")
        fp.write(conf33[0]+" \""+conf33[1]+"\" \""+conf33[2]+"\" \""+conf33[3]+"\"\n")
        fp.write(conf34[0]+" \""+conf34[1]+"\" \""+conf34[2]+"\" \""+conf34[3]+"\"\n")
        fp.write(conf35[0]+" \""+conf35[1]+"\" \""+conf35[2]+"\" \""+conf35[3]+"\"\n")
        fp.write(conf36[0]+" \""+conf36[1]+"\" \""+conf36[2]+"\" \""+conf36[3]+"\"\n")
        fp.write(conf37[0]+" \""+conf37[1]+"\" \""+conf37[2]+"\" \""+conf37[3]+"\"\n")
        fp.write(conf38[0]+" \""+conf38[1]+"\" \""+conf38[2]+"\" \""+conf38[3]+"\"\n")
        fp.write(conf39[0]+" \""+conf39[1]+"\" \""+conf39[2]+"\" \""+conf39[3]+"\"\n")
        fp.write(conf40[0]+" \""+conf40[1]+"\" \""+conf40[2]+"\" \""+conf40[3]+"\"\n")
        fp.write(conf41[0]+" \""+conf41[1]+"\" \""+conf41[2]+"\" \""+conf41[3]+"\"\n")
        fp.write(conf42[0]+" \""+conf42[1]+"\" \""+conf42[2]+"\" \""+conf42[3]+"\"\n")
        fp.write(conf43[0]+" \""+conf43[1]+"\" \""+conf43[2]+"\" \""+conf43[3]+"\"\n")
        fp.write(conf44[0]+" \""+conf44[1]+"\" \""+conf44[2]+"\" \""+conf44[3]+"\"\n")
        fp.write(conf45[0]+" \""+conf45[1]+"\" \""+conf45[2]+"\" \""+conf45[3]+"\"\n")
        fp.write(conf46[0]+" \""+conf46[1]+"\" \""+conf46[2]+"\" \""+conf46[3]+"\"\n")
        fp.write(conf47[0]+" \""+conf47[1]+"\" \""+conf47[2]+"\" \""+conf47[3]+"\"\n")
        fp.write(conf48[0]+" \""+conf48[1]+"\" \""+conf48[2]+"\" \""+conf48[3]+"\"\n")
        fp.write(conf49[0]+" \""+conf49[1]+"\" \""+conf49[2]+"\" \""+conf49[3]+"\"\n")
        fp.write(conf50[0]+" \""+conf50[1]+"\" \""+conf50[2]+"\" \""+conf50[3]+"\"\n")
        fp.write(conf51[0]+" \""+conf51[1]+"\" \""+conf51[2]+"\" \""+conf51[3]+"\"\n")
        fp.write(conf52[0]+" \""+conf52[1]+"\" \""+conf52[2]+"\" \""+conf52[3]+"\"\n")
        fp.write(conf53[0]+" \""+conf53[1]+"\" \""+conf53[2]+"\" \""+conf53[3]+"\"\n")
        fp.write(conf54[0]+" \""+conf54[1]+"\" \""+conf54[2]+"\" \""+conf54[3]+"\"\n")
        fp.write(conf55[0]+" \""+conf55[1]+"\" \""+conf55[2]+"\" \""+conf55[3]+"\"\n")
        fp.write(conf56[0]+" \""+conf56[1]+"\" \""+conf56[2]+"\" \""+conf56[3]+"\"\n")
        fp.write(conf57[0]+" \""+conf57[1]+"\" \""+conf57[2]+"\" \""+conf57[3]+"\"\n")
        fp.write(conf58[0]+" \""+conf58[1]+"\" \""+conf58[2]+"\" \""+conf58[3]+"\"\n")
        fp.write(conf59[0]+" \""+conf59[1]+"\" \""+conf59[2]+"\" \""+conf59[3]+"\"\n")
        fp.write(conf60[0]+" \""+conf60[1]+"\" \""+conf60[2]+"\" \""+conf60[3]+"\"\n")
        fp.write(conf61[0]+" \""+conf61[1]+"\" \""+conf61[2]+"\" \""+conf61[3]+"\"\n")
        fp.write(conf62[0]+" \""+conf62[1]+"\" \""+conf62[2]+"\" \""+conf62[3]+"\"\n")
        fp.write(conf63[0]+" \""+conf63[1]+"\" \""+conf63[2]+"\" \""+conf63[3]+"\"\n")
        fp.write(conf64[0]+" \""+conf64[1]+"\" \""+conf64[2]+"\" \""+conf64[3]+"\"\n")
        fp.write(conf65[0]+" \""+conf65[1]+"\" \""+conf65[2]+"\" \""+conf65[3]+"\"\n")
        fp.write(conf66[0]+" \""+conf66[1]+"\" \""+conf66[2]+"\" \""+conf66[3]+"\"\n")
        fp.write(conf67[0]+" \""+conf67[1]+"\" \""+conf67[2]+"\" \""+conf67[3]+"\"\n")
        fp.write(conf68[0]+" \""+conf68[1]+"\" \""+conf68[2]+"\" \""+conf68[3]+"\"\n")
        fp.write(conf69[0]+" \""+conf69[1]+"\" \""+conf69[2]+"\" \""+conf69[3]+"\"\n")
        fp.write(conf70[0]+" \""+conf70[1]+"\" \""+conf70[2]+"\" \""+conf70[3]+"\"\n")
        fp.write(conf71[0]+" \""+conf71[1]+"\" \""+conf71[2]+"\" \""+conf71[3]+"\"\n")
        fp.write(conf72[0]+" \""+conf72[1]+"\" \""+conf72[2]+"\" \""+conf72[3]+"\"\n")
        fp.write(conf73[0]+" \""+conf73[1]+"\" \""+conf73[2]+"\" \""+conf73[3]+"\"\n")
        fp.write(conf74[0]+" \""+conf74[1]+"\" \""+conf74[2]+"\" \""+conf74[3]+"\"\n")
        fp.write(conf75[0]+" \""+conf75[1]+"\" \""+conf75[2]+"\" \""+conf75[3]+"\"\n")
        fp.write(conf76[0]+" \""+conf76[1]+"\" \""+conf76[2]+"\" \""+conf76[3]+"\"\n")
        fp.write(conf77[0]+" \""+conf77[1]+"\" \""+conf77[2]+"\" \""+conf77[3]+"\"\n")
        fp.write(conf78[0]+" \""+conf78[1]+"\" \""+conf78[2]+"\" \""+conf78[3]+"\"\n")
        fp.write(conf79[0]+" \""+conf79[1]+"\" \""+conf79[2]+"\" \""+conf79[3]+"\"\n")
        fp.write(conf80[0]+" \""+conf80[1]+"\" \""+conf80[2]+"\" \""+conf80[3]+"\"\n")
        fp.write(conf81[0]+" \""+conf81[1]+"\" \""+conf81[2]+"\" \""+conf81[3]+"\"\n")
        fp.write(conf82[0]+" \""+conf82[1]+"\" \""+conf82[2]+"\" \""+conf82[3]+"\"\n")
        fp.write(conf83[0]+" \""+conf83[1]+"\" \""+conf83[2]+"\" \""+conf83[3]+"\"\n")
        fp.write(conf84[0]+" \""+conf84[1]+"\" \""+conf84[2]+"\" \""+conf84[3]+"\"\n")
        fp.write(conf85[0]+" \""+conf85[1]+"\" \""+conf85[2]+"\" \""+conf85[3]+"\"\n")
        fp.write(conf86[0]+" \""+conf86[1]+"\" \""+conf86[2]+"\" \""+conf86[3]+"\"\n")
        fp.write(conf87[0]+" \""+conf87[1]+"\" \""+conf87[2]+"\" \""+conf87[3]+"\"\n")
        fp.write(conf88[0]+" \""+conf88[1]+"\" \""+conf88[2]+"\" \""+conf88[3]+"\"\n")
        fp.write(conf89[0]+" \""+conf89[1]+"\" \""+conf89[2]+"\" \""+conf89[3]+"\"\n")
        fp.write(conf90[0]+" \""+conf90[1]+"\" \""+conf90[2]+"\" \""+conf90[3]+"\"\n")
        fp.write(conf91[0]+" \""+conf91[1]+"\" \""+conf91[2]+"\" \""+conf91[3]+"\"\n")
        fp.write(conf92[0]+" \""+conf92[1]+"\" \""+conf92[2]+"\" \""+conf92[3]+"\"\n")
        fp.write(conf93[0]+" \""+conf93[1]+"\" \""+conf93[2]+"\" \""+conf93[3]+"\"\n")
        fp.write(conf94[0]+" \""+conf94[1]+"\" \""+conf94[2]+"\" \""+conf94[3]+"\"\n")
        fp.write(conf95[0]+" \""+conf95[1]+"\" \""+conf95[2]+"\" \""+conf95[3]+"\"\n")
        fp.write(conf96[0]+" \""+conf96[1]+"\" \""+conf96[2]+"\" \""+conf96[3]+"\"\n")
        fp.write(conf97[0]+" \""+conf97[1]+"\" \""+conf97[2]+"\" \""+conf97[3]+"\"\n")
        fp.write(conf98[0]+" \""+conf98[1]+"\" \""+conf98[2]+"\" \""+conf98[3]+"\"\n")
        fp.write(conf99[0]+" \""+conf99[1]+"\" \""+conf99[2]+"\" \""+conf99[3]+"\"\n")
        fp.write(conf100[0]+" \""+conf100[1]+"\" \""+conf100[2]+"\" \""+conf100[3]+"\"\n")
        fp.write(conf101[0]+" \""+conf101[1]+"\" \""+conf101[2]+"\" \""+conf101[3]+"\"\n")
        fp.write(conf102[0]+" \""+conf102[1]+"\" \""+conf102[2]+"\" \""+conf102[3]+"\"\n")
        fp.write(conf103[0]+" \""+conf103[1]+"\" \""+conf103[2]+"\" \""+conf103[3]+"\"\n")
        fp.write(conf104[0]+" \""+conf104[1]+"\" \""+conf104[2]+"\" \""+conf104[3]+"\"\n")
        fp.write(conf105[0]+" \""+conf105[1]+"\" \""+conf105[2]+"\" \""+conf105[3]+"\"\n")
        fp.write(conf106[0]+" \""+conf106[1]+"\" \""+conf106[2]+"\" \""+conf106[3]+"\"\n")
        fp.write(conf107[0]+" \""+conf107[1]+"\" \""+conf107[2]+"\" \""+conf107[3]+"\"\n")
        fp.write(conf108[0]+" \""+conf108[1]+"\" \""+conf108[2]+"\" \""+conf108[3]+"\"\n")
        fp.write(conf109[0]+" \""+conf109[1]+"\" \""+conf109[2]+"\" \""+conf109[3]+"\"\n")
        fp.write(conf110[0]+" \""+conf110[1]+"\" \""+conf110[2]+"\" \""+conf110[3]+"\"\n")
        fp.write(conf111[0]+" \""+conf111[1]+"\" \""+conf111[2]+"\" \""+conf111[3]+"\"\n")
        fp.write(conf112[0]+" \""+conf112[1]+"\" \""+conf112[2]+"\" \""+conf112[3]+"\"\n")
        fp.write(conf113[0]+" \""+conf113[1]+"\" \""+conf113[2]+"\" \""+conf113[3]+"\"\n")
        fp.write(conf114[0]+" \""+conf114[1]+"\" \""+conf114[2]+"\" \""+conf114[3]+"\"\n")
        fp.write(conf115[0]+" \""+conf115[1]+"\" \""+conf115[2]+"\" \""+conf115[3]+"\"\n")
        fp.write(conf116[0]+" \""+conf116[1]+"\" \""+conf116[2]+"\" \""+conf116[3]+"\"\n")
        fp.write(conf117[0]+" \""+conf117[1]+"\" \""+conf117[2]+"\" \""+conf117[3]+"\"\n")
        fp.write(conf118[0]+" \""+conf118[1]+"\" \""+conf118[2]+"\" \""+conf118[3]+"\"\n")
        fp.write(conf119[0]+" \""+conf119[1]+"\" \""+conf119[2]+"\" \""+conf119[3]+"\"\n")
        fp.write(conf120[0]+" \""+conf120[1]+"\" \""+conf120[2]+"\" \""+conf120[3]+"\"\n")
        fp.write(conf121[0]+" \""+conf121[1]+"\" \""+conf121[2]+"\" \""+conf121[3]+"\"\n")
        fp.write(conf122[0]+" \""+conf122[1]+"\" \""+conf122[2]+"\" \""+conf122[3]+"\"\n")
        fp.write(conf123[0]+" \""+conf123[1]+"\" \""+conf123[2]+"\" \""+conf123[3]+"\"\n")
        fp.write(conf124[0]+" \""+conf124[1]+"\" \""+conf124[2]+"\" \""+conf124[3]+"\"\n")
        fp.write(conf125[0]+" \""+conf125[1]+"\" \""+conf125[2]+"\" \""+conf125[3]+"\"\n")
        fp.write(conf126[0]+" \""+conf126[1]+"\" \""+conf126[2]+"\" \""+conf126[3]+"\"\n")
        fp.write(conf127[0]+" \""+conf127[1]+"\" \""+conf127[2]+"\" \""+conf127[3]+"\"\n")
        fp.write(conf128[0]+" \""+conf128[1]+"\" \""+conf128[2]+"\" \""+conf128[3]+"\"\n")
        fp.write(conf129[0]+" \""+conf129[1]+"\" \""+conf129[2]+"\" \""+conf129[3]+"\"\n")
        fp.write(conf130[0]+" \""+conf130[1]+"\" \""+conf130[2]+"\" \""+conf130[3]+"\"\n")
        fp.write(conf131[0]+" \""+conf131[1]+"\" \""+conf131[2]+"\" \""+conf131[3]+"\"\n")
        fp.write(conf132[0]+" \""+conf132[1]+"\" \""+conf132[2]+"\" \""+conf132[3]+"\"\n")
        fp.write(conf133[0]+" \""+conf133[1]+"\" \""+conf133[2]+"\" \""+conf133[3]+"\"\n")
        fp.write(conf134[0]+" \""+conf134[1]+"\" \""+conf134[2]+"\" \""+conf134[3]+"\"\n")
        fp.write(conf135[0]+" \""+conf135[1]+"\" \""+conf135[2]+"\" \""+conf135[3]+"\"\n")
        fp.write(conf136[0]+" \""+conf136[1]+"\" \""+conf136[2]+"\" \""+conf136[3]+"\"\n")
        fp.write(conf137[0]+" \""+conf137[1]+"\" \""+conf137[2]+"\" \""+conf137[3]+"\"\n")
        fp.write(conf138[0]+" \""+conf138[1]+"\" \""+conf138[2]+"\" \""+conf138[3]+"\"\n")
        fp.write(conf139[0]+" \""+conf139[1]+"\" \""+conf139[2]+"\" \""+conf139[3]+"\"\n")
        fp.write(conf140[0]+" \""+conf140[1]+"\" \""+conf140[2]+"\" \""+conf140[3]+"\"\n")
        fp.write(conf141[0]+" \""+conf141[1]+"\" \""+conf141[2]+"\" \""+conf141[3]+"\"\n")
        fp.write(conf142[0]+" \""+conf142[1]+"\" \""+conf142[2]+"\" \""+conf142[3]+"\"\n")
        fp.write(conf143[0]+" \""+conf143[1]+"\" \""+conf143[2]+"\" \""+conf143[3]+"\"\n")
        fp.write(conf144[0]+" \""+conf144[1]+"\" \""+conf144[2]+"\" \""+conf144[3]+"\"\n")
        fp.write(conf145[0]+" \""+conf145[1]+"\" \""+conf145[2]+"\" \""+conf145[3]+"\"\n")
        fp.write(conf146[0]+" \""+conf146[1]+"\" \""+conf146[2]+"\" \""+conf146[3]+"\"\n")
        fp.write(conf147[0]+" \""+conf147[1]+"\" \""+conf147[2]+"\" \""+conf147[3]+"\"\n")
        fp.write(conf148[0]+" \""+conf148[1]+"\" \""+conf148[2]+"\" \""+conf148[3]+"\"\n")
        fp.write(conf149[0]+" \""+conf149[1]+"\" \""+conf149[2]+"\" \""+conf149[3]+"\"\n")
        fp.write(conf150[0]+" \""+conf150[1]+"\" \""+conf150[2]+"\" \""+conf150[3]+"\"\n")
        fp.write(conf151[0]+" \""+conf151[1]+"\" \""+conf151[2]+"\" \""+conf151[3]+"\"\n")
        fp.write(conf152[0]+" \""+conf152[1]+"\" \""+conf152[2]+"\" \""+conf152[3]+"\"\n")
        fp.write(conf153[0]+" \""+conf153[1]+"\" \""+conf153[2]+"\" \""+conf153[3]+"\"\n")
        fp.write(conf154[0]+" \""+conf154[1]+"\" \""+conf154[2]+"\" \""+conf154[3]+"\"\n")
        fp.write(conf155[0]+" \""+conf155[1]+"\" \""+conf155[2]+"\" \""+conf155[3]+"\"\n")
        fp.write(conf156[0]+" \""+conf156[1]+"\" \""+conf156[2]+"\" \""+conf156[3]+"\"\n")
        fp.write(conf157[0]+" \""+conf157[1]+"\" \""+conf157[2]+"\" \""+conf157[3]+"\"\n")
        fp.write(conf158[0]+" \""+conf158[1]+"\" \""+conf158[2]+"\" \""+conf158[3]+"\"\n")
        fp.write(conf159[0]+" \""+conf159[1]+"\" \""+conf159[2]+"\" \""+conf159[3]+"\"\n")
        fp.write(conf160[0]+" \""+conf160[1]+"\" \""+conf160[2]+"\" \""+conf160[3]+"\"\n")
        fp.write(conf161[0]+" \""+conf161[1]+"\" \""+conf161[2]+"\" \""+conf161[3]+"\"\n")
        fp.write(conf162[0]+" \""+conf162[1]+"\" \""+conf162[2]+"\" \""+conf162[3]+"\"\n")
        fp.write(conf163[0]+" \""+conf163[1]+"\" \""+conf163[2]+"\" \""+conf163[3]+"\"\n")
        fp.write(conf164[0]+" \""+conf164[1]+"\" \""+conf164[2]+"\" \""+conf164[3]+"\"\n")
        fp.write(conf165[0]+" \""+conf165[1]+"\" \""+conf165[2]+"\" \""+conf165[3]+"\"\n")
        fp.write(conf166[0]+" \""+conf166[1]+"\" \""+conf166[2]+"\" \""+conf166[3]+"\"\n")
        fp.write(conf167[0]+" \""+conf167[1]+"\" \""+conf167[2]+"\" \""+conf167[3]+"\"\n")
        fp.write(conf168[0]+" \""+conf168[1]+"\" \""+conf168[2]+"\" \""+conf168[3]+"\"\n")
        fp.write(conf169[0]+" \""+conf169[1]+"\" \""+conf169[2]+"\" \""+conf169[3]+"\"\n")
        fp.write(conf170[0]+" \""+conf170[1]+"\" \""+conf170[2]+"\" \""+conf170[3]+"\"\n")
        fp.write(conf171[0]+" \""+conf171[1]+"\" \""+conf171[2]+"\" \""+conf171[3]+"\"\n")
        fp.write(conf172[0]+" \""+conf172[1]+"\" \""+conf172[2]+"\" \""+conf172[3]+"\"\n")
        fp.write(conf173[0]+" \""+conf173[1]+"\" \""+conf173[2]+"\" \""+conf173[3]+"\"\n")
        fp.write(conf174[0]+" \""+conf174[1]+"\" \""+conf174[2]+"\" \""+conf174[3]+"\"\n")
        fp.write(conf175[0]+" \""+conf175[1]+"\" \""+conf175[2]+"\" \""+conf175[3]+"\"\n")
        fp.write(conf176[0]+" \""+conf176[1]+"\" \""+conf176[2]+"\" \""+conf176[3]+"\"\n")
        fp.write(conf177[0]+" \""+conf177[1]+"\" \""+conf177[2]+"\" \""+conf177[3]+"\"\n")
        fp.write(conf178[0]+" \""+conf178[1]+"\" \""+conf178[2]+"\" \""+conf178[3]+"\"\n")
        fp.write(conf179[0]+" \""+conf179[1]+"\" \""+conf179[2]+"\" \""+conf179[3]+"\"\n")
        fp.write(conf180[0]+" \""+conf180[1]+"\" \""+conf180[2]+"\" \""+conf180[3]+"\"\n")
        fp.write(conf181[0]+" \""+conf181[1]+"\" \""+conf181[2]+"\" \""+conf181[3]+"\"\n")
        fp.write(conf182[0]+" \""+conf182[1]+"\" \""+conf182[2]+"\" \""+conf182[3]+"\"\n")
        fp.write(conf183[0]+" \""+conf183[1]+"\" \""+conf183[2]+"\" \""+conf183[3]+"\"\n")
        fp.write(conf184[0]+" \""+conf184[1]+"\" \""+conf184[2]+"\" \""+conf184[3]+"\"\n")
        fp.write(conf185[0]+" \""+conf185[1]+"\" \""+conf185[2]+"\" \""+conf185[3]+"\"\n")
        fp.write(conf186[0]+" \""+conf186[1]+"\" \""+conf186[2]+"\" \""+conf186[3]+"\"\n")
        fp.write(conf187[0]+" \""+conf187[1]+"\" \""+conf187[2]+"\" \""+conf187[3]+"\"\n")
        fp.write(conf188[0]+" \""+conf188[1]+"\" \""+conf188[2]+"\" \""+conf188[3]+"\"\n")
        fp.write(conf189[0]+" \""+conf189[1]+"\" \""+conf189[2]+"\" \""+conf189[3]+"\"\n")
        fp.write(conf190[0]+" \""+conf190[1]+"\" \""+conf190[2]+"\" \""+conf190[3]+"\"\n")
        fp.write(conf191[0]+" \""+conf191[1]+"\" \""+conf191[2]+"\" \""+conf191[3]+"\"\n")
        fp.write(conf192[0]+" \""+conf192[1]+"\" \""+conf192[2]+"\" \""+conf192[3]+"\"\n")
        fp.write(conf193[0]+" \""+conf193[1]+"\" \""+conf193[2]+"\" \""+conf193[3]+"\"\n")
        fp.write(conf194[0]+" \""+conf194[1]+"\" \""+conf194[2]+"\" \""+conf194[3]+"\"\n")
        fp.write(conf195[0]+" \""+conf195[1]+"\" \""+conf195[2]+"\" \""+conf195[3]+"\"\n")
        fp.write(conf196[0]+" \""+conf196[1]+"\" \""+conf196[2]+"\" \""+conf196[3]+"\"\n")
        fp.write(conf197[0]+" \""+conf197[1]+"\" \""+conf197[2]+"\" \""+conf197[3]+"\"\n")
        fp.write(conf198[0]+" \""+conf198[1]+"\" \""+conf198[2]+"\" \""+conf198[3]+"\"\n")
        fp.write(conf199[0]+" \""+conf199[1]+"\" \""+conf199[2]+"\" \""+conf199[3]+"\"\n")
        fp.write(conf200[0]+" \""+conf200[1]+"\" \""+conf200[2]+"\" \""+conf200[3]+"\"\n")
        fp.write(conf201[0]+" \""+conf201[1]+"\" \""+conf201[2]+"\" \""+conf201[3]+"\"\n")
        fp.write(conf202[0]+" \""+conf202[1]+"\" \""+conf202[2]+"\" \""+conf202[3]+"\"\n")
        fp.write(conf203[0]+" \""+conf203[1]+"\" \""+conf203[2]+"\" \""+conf203[3]+"\"\n")
        fp.write(conf204[0]+" \""+conf204[1]+"\" \""+conf204[2]+"\" \""+conf204[3]+"\"\n")
        fp.write(conf205[0]+" \""+conf205[1]+"\" \""+conf205[2]+"\" \""+conf205[3]+"\"\n")
        fp.write(conf206[0]+" \""+conf206[1]+"\" \""+conf206[2]+"\" \""+conf206[3]+"\"\n")
        fp.write(conf207[0]+" \""+conf207[1]+"\" \""+conf207[2]+"\" \""+conf207[3]+"\"\n")
        fp.write(conf208[0]+" \""+conf208[1]+"\" \""+conf208[2]+"\" \""+conf208[3]+"\"\n")
        fp.write(conf209[0]+" \""+conf209[1]+"\" \""+conf209[2]+"\" \""+conf209[3]+"\"\n")
        fp.write(conf210[0]+" \""+conf210[1]+"\" \""+conf210[2]+"\" \""+conf210[3]+"\"\n")
        fp.write(conf211[0]+" \""+conf211[1]+"\" \""+conf211[2]+"\" \""+conf211[3]+"\"\n")
        fp.write(conf212[0]+" \""+conf212[1]+"\" \""+conf212[2]+"\" \""+conf212[3]+"\"\n")
        fp.write(conf213[0]+" \""+conf213[1]+"\" \""+conf213[2]+"\" \""+conf213[3]+"\"\n")
        fp.write(conf214[0]+" \""+conf214[1]+"\" \""+conf214[2]+"\" \""+conf214[3]+"\"\n")
        fp.write(conf215[0]+" \""+conf215[1]+"\" \""+conf215[2]+"\" \""+conf215[3]+"\"\n")
        fp.write(conf216[0]+" \""+conf216[1]+"\" \""+conf216[2]+"\" \""+conf216[3]+"\"\n")
        fp.write(conf217[0]+" \""+conf217[1]+"\" \""+conf217[2]+"\" \""+conf217[3]+"\"\n")
        fp.write(conf218[0]+" \""+conf218[1]+"\" \""+conf218[2]+"\" \""+conf218[3]+"\"\n")
        fp.write(conf219[0]+" \""+conf219[1]+"\" \""+conf219[2]+"\" \""+conf219[3]+"\"\n")
        fp.write(conf220[0]+" \""+conf220[1]+"\" \""+conf220[2]+"\" \""+conf220[3]+"\"\n")
        fp.write(conf221[0]+" \""+conf221[1]+"\" \""+conf221[2]+"\" \""+conf221[3]+"\"\n")
        fp.write(conf222[0]+" \""+conf222[1]+"\" \""+conf222[2]+"\" \""+conf222[3]+"\"\n")
        fp.write(conf223[0]+" \""+conf223[1]+"\" \""+conf223[2]+"\" \""+conf223[3]+"\"\n")
        fp.write(conf224[0]+" \""+conf224[1]+"\" \""+conf224[2]+"\" \""+conf224[3]+"\"\n")
        fp.write(conf225[0]+" \""+conf225[1]+"\" \""+conf225[2]+"\" \""+conf225[3]+"\"\n")
        fp.write(conf226[0]+" \""+conf226[1]+"\" \""+conf226[2]+"\" \""+conf226[3]+"\"\n")
        fp.write(conf227[0]+" \""+conf227[1]+"\" \""+conf227[2]+"\" \""+conf227[3]+"\"\n")
        fp.write(conf228[0]+" \""+conf228[1]+"\" \""+conf228[2]+"\" \""+conf228[3]+"\"\n")
        fp.write(conf229[0]+" \""+conf229[1]+"\" \""+conf229[2]+"\" \""+conf229[3]+"\"\n")
        fp.write(conf230[0]+" \""+conf230[1]+"\" \""+conf230[2]+"\" \""+conf230[3]+"\"\n")
        fp.write(conf231[0]+" \""+conf231[1]+"\" \""+conf231[2]+"\" \""+conf231[3]+"\"\n")
        fp.write(conf232[0]+" \""+conf232[1]+"\" \""+conf232[2]+"\" \""+conf232[3]+"\"\n")
        fp.write(conf233[0]+" \""+conf233[1]+"\" \""+conf233[2]+"\" \""+conf233[3]+"\"\n")
        fp.write(conf234[0]+" \""+conf234[1]+"\" \""+conf234[2]+"\" \""+conf234[3]+"\"\n")
        fp.write(conf235[0]+" \""+conf235[1]+"\" \""+conf235[2]+"\" \""+conf235[3]+"\"\n")
        fp.write(conf236[0]+" \""+conf236[1]+"\" \""+conf236[2]+"\" \""+conf236[3]+"\"\n")
        fp.write(conf237[0]+" \""+conf237[1]+"\" \""+conf237[2]+"\" \""+conf237[3]+"\"\n")
        fp.write(conf238[0]+" \""+conf238[1]+"\" \""+conf238[2]+"\" \""+conf238[3]+"\"\n")
        fp.write(conf239[0]+" \""+conf239[1]+"\" \""+conf239[2]+"\" \""+conf239[3]+"\"\n")
        fp.write(conf240[0]+" \""+conf240[1]+"\" \""+conf240[2]+"\" \""+conf240[3]+"\"\n")
        fp.write(conf241[0]+" \""+conf241[1]+"\" \""+conf241[2]+"\" \""+conf241[3]+"\"\n")
        fp.write(conf242[0]+" \""+conf242[1]+"\" \""+conf242[2]+"\" \""+conf242[3]+"\"\n")
        fp.write(conf243[0]+" \""+conf243[1]+"\" \""+conf243[2]+"\" \""+conf243[3]+"\"\n")
        fp.write(conf244[0]+" \""+conf244[1]+"\" \""+conf244[2]+"\" \""+conf244[3]+"\"\n")
        fp.write(conf245[0]+" \""+conf245[1]+"\" \""+conf245[2]+"\" \""+conf245[3]+"\"\n")
        fp.write(conf246[0]+" \""+conf246[1]+"\" \""+conf246[2]+"\" \""+conf246[3]+"\"\n")
        fp.write(conf247[0]+" \""+conf247[1]+"\" \""+conf247[2]+"\" \""+conf247[3]+"\"\n")
        fp.write(conf248[0]+" \""+conf248[1]+"\" \""+conf248[2]+"\" \""+conf248[3]+"\"\n")
        fp.write(conf249[0]+" \""+conf249[1]+"\" \""+conf249[2]+"\" \""+conf249[3]+"\"\n")
        fp.write(conf250[0]+" \""+conf250[1]+"\" \""+conf250[2]+"\" \""+conf250[3]+"\"\n")
        fp.write(conf251[0]+" \""+conf251[1]+"\" \""+conf251[2]+"\" \""+conf251[3]+"\"\n")
        fp.write(conf252[0]+" \""+conf252[1]+"\" \""+conf252[2]+"\" \""+conf252[3]+"\"\n")
        fp.write(conf253[0]+" \""+conf253[1]+"\" \""+conf253[2]+"\" \""+conf253[3]+"\"\n")
        fp.write(conf254[0]+" \""+conf254[1]+"\" \""+conf254[2]+"\" \""+conf254[3]+"\"\n")
        fp.write(conf255[0]+" \""+conf255[1]+"\" \""+conf255[2]+"\" \""+conf255[3]+"\"\n")
        fp.write(conf256[0]+" \""+conf256[1]+"\" \""+conf256[2]+"\" \""+conf256[3]+"\"\n")
        fp.write(conf257[0]+" \""+conf257[1]+"\" \""+conf257[2]+"\" \""+conf257[3]+"\"\n")
        fp.write(conf258[0]+" \""+conf258[1]+"\" \""+conf258[2]+"\" \""+conf258[3]+"\"\n")
        fp.write(conf259[0]+" \""+conf259[1]+"\" \""+conf259[2]+"\" \""+conf259[3]+"\"\n")
        fp.write(conf260[0]+" \""+conf260[1]+"\" \""+conf260[2]+"\" \""+conf260[3]+"\"\n")
        fp.write(conf261[0]+" \""+conf261[1]+"\" \""+conf261[2]+"\" \""+conf261[3]+"\"\n")
        fp.write(conf262[0]+" \""+conf262[1]+"\" \""+conf262[2]+"\" \""+conf262[3]+"\"\n")
        fp.write(conf263[0]+" \""+conf263[1]+"\" \""+conf263[2]+"\" \""+conf263[3]+"\"\n")
        fp.write(conf264[0]+" \""+conf264[1]+"\" \""+conf264[2]+"\" \""+conf264[3]+"\"\n")
        fp.write(conf265[0]+" \""+conf265[1]+"\" \""+conf265[2]+"\" \""+conf265[3]+"\"\n")
        fp.write(conf266[0]+" \""+conf266[1]+"\" \""+conf266[2]+"\" \""+conf266[3]+"\"\n")
        fp.write(conf267[0]+" \""+conf267[1]+"\" \""+conf267[2]+"\" \""+conf267[3]+"\"\n")
        fp.write(conf268[0]+" \""+conf268[1]+"\" \""+conf268[2]+"\" \""+conf268[3]+"\"\n")
        fp.write(conf269[0]+" \""+conf269[1]+"\" \""+conf269[2]+"\" \""+conf269[3]+"\"\n")
        fp.write(conf270[0]+" \""+conf270[1]+"\" \""+conf270[2]+"\" \""+conf270[3]+"\"\n")
        fp.write(conf271[0]+" \""+conf271[1]+"\" \""+conf271[2]+"\" \""+conf271[3]+"\"\n")
        fp.write(conf272[0]+" \""+conf272[1]+"\" \""+conf272[2]+"\" \""+conf272[3]+"\"\n")
        fp.write(conf273[0]+" \""+conf273[1]+"\" \""+conf273[2]+"\" \""+conf273[3]+"\"\n")
        fp.write(conf274[0]+" \""+conf274[1]+"\" \""+conf274[2]+"\" \""+conf274[3]+"\"\n")
        fp.write(conf275[0]+" \""+conf275[1]+"\" \""+conf275[2]+"\" \""+conf275[3]+"\"\n")
        fp.write(conf276[0]+" \""+conf276[1]+"\" \""+conf276[2]+"\" \""+conf276[3]+"\"\n")
        fp.write(conf277[0]+" \""+conf277[1]+"\" \""+conf277[2]+"\" \""+conf277[3]+"\"\n")
        fp.write(conf278[0]+" \""+conf278[1]+"\" \""+conf278[2]+"\" \""+conf278[3]+"\"\n")
        fp.write(conf279[0]+" \""+conf279[1]+"\" \""+conf279[2]+"\" \""+conf279[3]+"\"\n")
        fp.write(conf280[0]+" \""+conf280[1]+"\" \""+conf280[2]+"\" \""+conf280[3]+"\"\n")
        fp.write(conf281[0]+" \""+conf281[1]+"\" \""+conf281[2]+"\" \""+conf281[3]+"\"\n")
        fp.write(conf282[0]+" \""+conf282[1]+"\" \""+conf282[2]+"\" \""+conf282[3]+"\"\n")
        fp.write(conf283[0]+" \""+conf283[1]+"\" \""+conf283[2]+"\" \""+conf283[3]+"\"\n")
        fp.write(conf284[0]+" \""+conf284[1]+"\" \""+conf284[2]+"\" \""+conf284[3]+"\"\n")
        fp.write(conf285[0]+" \""+conf285[1]+"\" \""+conf285[2]+"\" \""+conf285[3]+"\"\n")
        fp.write(conf286[0]+" \""+conf286[1]+"\" \""+conf286[2]+"\" \""+conf286[3]+"\"\n")
        fp.write(conf287[0]+" \""+conf287[1]+"\" \""+conf287[2]+"\" \""+conf287[3]+"\"\n")
        fp.write(conf288[0]+" \""+conf288[1]+"\" \""+conf288[2]+"\" \""+conf288[3]+"\"\n")
        fp.write(conf289[0]+" \""+conf289[1]+"\" \""+conf289[2]+"\" \""+conf289[3]+"\"\n")
        fp.write(conf290[0]+" \""+conf290[1]+"\" \""+conf290[2]+"\" \""+conf290[3]+"\"\n")
        fp.write(conf291[0]+" \""+conf291[1]+"\" \""+conf291[2]+"\" \""+conf291[3]+"\"\n")
        fp.write(conf292[0]+" \""+conf292[1]+"\" \""+conf292[2]+"\" \""+conf292[3]+"\"\n")
        fp.write(conf293[0]+" \""+conf293[1]+"\" \""+conf293[2]+"\" \""+conf293[3]+"\"\n")
        fp.write(conf294[0]+" \""+conf294[1]+"\" \""+conf294[2]+"\" \""+conf294[3]+"\"\n")
        fp.write(conf295[0]+" \""+conf295[1]+"\" \""+conf295[2]+"\" \""+conf295[3]+"\"\n")
        fp.write(conf296[0]+" \""+conf296[1]+"\" \""+conf296[2]+"\" \""+conf296[3]+"\"\n")
        fp.write(conf297[0]+" \""+conf297[1]+"\" \""+conf297[2]+"\" \""+conf297[3]+"\"\n")
        fp.write(conf298[0]+" \""+conf298[1]+"\" \""+conf298[2]+"\" \""+conf298[3]+"\"\n")
        fp.write(conf299[0]+" \""+conf299[1]+"\" \""+conf299[2]+"\" \""+conf299[3]+"\"\n")
        fp.write(conf300[0]+" \""+conf300[1]+"\" \""+conf300[2]+"\" \""+conf300[3]+"\"\n")
        fp.write(conf301[0]+" \""+conf301[1]+"\" \""+conf301[2]+"\" \""+conf301[3]+"\"\n")
        fp.write(conf302[0]+" \""+conf302[1]+"\" \""+conf302[2]+"\" \""+conf302[3]+"\"\n")
        fp.write(conf303[0]+" \""+conf303[1]+"\" \""+conf303[2]+"\" \""+conf303[3]+"\"\n")
        fp.write(conf304[0]+" \""+conf304[1]+"\" \""+conf304[2]+"\" \""+conf304[3]+"\"\n")
        fp.write(conf305[0]+" \""+conf305[1]+"\" \""+conf305[2]+"\" \""+conf305[3]+"\"\n")
        fp.write(conf306[0]+" \""+conf306[1]+"\" \""+conf306[2]+"\" \""+conf306[3]+"\"\n")
        fp.write(conf307[0]+" \""+conf307[1]+"\" \""+conf307[2]+"\" \""+conf307[3]+"\"\n")
        fp.write(conf308[0]+" \""+conf308[1]+"\" \""+conf308[2]+"\" \""+conf308[3]+"\"\n")
        fp.write(conf309[0]+" \""+conf309[1]+"\" \""+conf309[2]+"\" \""+conf309[3]+"\"\n")
        fp.write(conf310[0]+" \""+conf310[1]+"\" \""+conf310[2]+"\" \""+conf310[3]+"\"\n")
        fp.write(conf311[0]+" \""+conf311[1]+"\" \""+conf311[2]+"\" \""+conf311[3]+"\"\n")
        fp.write(conf312[0]+" \""+conf312[1]+"\" \""+conf312[2]+"\" \""+conf312[3]+"\"\n")
        fp.write(conf313[0]+" \""+conf313[1]+"\" \""+conf313[2]+"\" \""+conf313[3]+"\"\n")
        fp.write(conf314[0]+" \""+conf314[1]+"\" \""+conf314[2]+"\" \""+conf314[3]+"\"\n")
        fp.write(conf315[0]+" \""+conf315[1]+"\" \""+conf315[2]+"\" \""+conf315[3]+"\"\n")
        fp.write(conf316[0]+" \""+conf316[1]+"\" \""+conf316[2]+"\" \""+conf316[3]+"\"\n")
        fp.write(conf317[0]+" \""+conf317[1]+"\" \""+conf317[2]+"\" \""+conf317[3]+"\"\n")
        fp.write(conf318[0]+" \""+conf318[1]+"\" \""+conf318[2]+"\" \""+conf318[3]+"\"\n")
        fp.write(conf319[0]+" \""+conf319[1]+"\" \""+conf319[2]+"\" \""+conf319[3]+"\"\n")
        fp.write(conf320[0]+" \""+conf320[1]+"\" \""+conf320[2]+"\" \""+conf320[3]+"\"\n")
        fp.write(conf321[0]+" \""+conf321[1]+"\" \""+conf321[2]+"\" \""+conf321[3]+"\"\n")
        fp.write(conf322[0]+" \""+conf322[1]+"\" \""+conf322[2]+"\" \""+conf322[3]+"\"\n")
        fp.write(conf323[0]+" \""+conf323[1]+"\" \""+conf323[2]+"\" \""+conf323[3]+"\"\n")
        fp.write(conf324[0]+" \""+conf324[1]+"\" \""+conf324[2]+"\" \""+conf324[3]+"\"\n")
        fp.write(conf325[0]+" \""+conf325[1]+"\" \""+conf325[2]+"\" \""+conf325[3]+"\"\n")
        fp.write(conf326[0]+" \""+conf326[1]+"\" \""+conf326[2]+"\" \""+conf326[3]+"\"\n")
        fp.write(conf327[0]+" \""+conf327[1]+"\" \""+conf327[2]+"\" \""+conf327[3]+"\"\n")
        fp.write(conf328[0]+" \""+conf328[1]+"\" \""+conf328[2]+"\" \""+conf328[3]+"\"\n")
        fp.write(conf329[0]+" \""+conf329[1]+"\" \""+conf329[2]+"\" \""+conf329[3]+"\"\n")
        fp.write(conf330[0]+" \""+conf330[1]+"\" \""+conf330[2]+"\" \""+conf330[3]+"\"\n")
        fp.write(conf331[0]+" \""+conf331[1]+"\" \""+conf331[2]+"\" \""+conf331[3]+"\"\n")
        fp.write(conf332[0]+" \""+conf332[1]+"\" \""+conf332[2]+"\" \""+conf332[3]+"\"\n")
        fp.write(conf333[0]+" \""+conf333[1]+"\" \""+conf333[2]+"\" \""+conf333[3]+"\"\n")
        fp.write(conf334[0]+" \""+conf334[1]+"\" \""+conf334[2]+"\" \""+conf334[3]+"\"\n")
        fp.write(conf335[0]+" \""+conf335[1]+"\" \""+conf335[2]+"\" \""+conf335[3]+"\"\n")
        fp.write(conf336[0]+" \""+conf336[1]+"\" \""+conf336[2]+"\" \""+conf336[3]+"\"\n")
        fp.write(conf337[0]+" \""+conf337[1]+"\" \""+conf337[2]+"\" \""+conf337[3]+"\"\n")
        fp.write(conf338[0]+" \""+conf338[1]+"\" \""+conf338[2]+"\" \""+conf338[3]+"\"\n")
        fp.write(conf339[0]+" \""+conf339[1]+"\" \""+conf339[2]+"\" \""+conf339[3]+"\"\n")
        fp.write(conf340[0]+" \""+conf340[1]+"\" \""+conf340[2]+"\" \""+conf340[3]+"\"\n")
        fp.write(conf341[0]+" \""+conf341[1]+"\" \""+conf341[2]+"\" \""+conf341[3]+"\"\n")
        fp.write(conf342[0]+" \""+conf342[1]+"\" \""+conf342[2]+"\" \""+conf342[3]+"\"\n")
        fp.write(conf343[0]+" \""+conf343[1]+"\" \""+conf343[2]+"\" \""+conf343[3]+"\"\n")
        fp.write(conf344[0]+" \""+conf344[1]+"\" \""+conf344[2]+"\" \""+conf344[3]+"\"\n")
        fp.write(conf345[0]+" \""+conf345[1]+"\" \""+conf345[2]+"\" \""+conf345[3]+"\"\n")
        fp.write(conf346[0]+" \""+conf346[1]+"\" \""+conf346[2]+"\" \""+conf346[3]+"\"\n")
        fp.write(conf347[0]+" \""+conf347[1]+"\" \""+conf347[2]+"\" \""+conf347[3]+"\"\n")
        fp.write(conf348[0]+" \""+conf348[1]+"\" \""+conf348[2]+"\" \""+conf348[3]+"\"\n")
        fp.write(conf349[0]+" \""+conf349[1]+"\" \""+conf349[2]+"\" \""+conf349[3]+"\"\n")
        fp.write(conf350[0]+" \""+conf350[1]+"\" \""+conf350[2]+"\" \""+conf350[3]+"\"\n")
        fp.write(conf351[0]+" \""+conf351[1]+"\" \""+conf351[2]+"\" \""+conf351[3]+"\"\n")
        fp.write(conf352[0]+" \""+conf352[1]+"\" \""+conf352[2]+"\" \""+conf352[3]+"\"\n")
        fp.write(conf353[0]+" \""+conf353[1]+"\" \""+conf353[2]+"\" \""+conf353[3]+"\"\n")
        fp.write(conf354[0]+" \""+conf354[1]+"\" \""+conf354[2]+"\" \""+conf354[3]+"\"\n")
        fp.write(conf355[0]+" \""+conf355[1]+"\" \""+conf355[2]+"\" \""+conf355[3]+"\"\n")
        fp.write(conf356[0]+" \""+conf356[1]+"\" \""+conf356[2]+"\" \""+conf356[3]+"\"\n")
        fp.write(conf357[0]+" \""+conf357[1]+"\" \""+conf357[2]+"\" \""+conf357[3]+"\"\n")
        fp.write(conf358[0]+" \""+conf358[1]+"\" \""+conf358[2]+"\" \""+conf358[3]+"\"\n")
        fp.write(conf359[0]+" \""+conf359[1]+"\" \""+conf359[2]+"\" \""+conf359[3]+"\"\n")
        fp.write(conf360[0]+" \""+conf360[1]+"\" \""+conf360[2]+"\" \""+conf360[3]+"\"\n")
        fp.close()
        os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)
    #
    #   For game settings local which is also required
    def createFileLocal(self,file):
        if exists(file):
            os.chmod(file,stat.S_IWRITE )
        fp = open(file, 'w')
        fp.write(conf237[0]+" \""+conf237[1]+"\" \""+conf237[2]+"\" \""+conf237[3]+"\"\n")
        fp.write(conf223[0]+" \""+conf223[1]+"\" \""+conf223[2]+"\" \""+conf223[3]+"\"\n")
        fp.write(conf235[0]+" \""+conf235[1]+"\" \""+conf235[2]+"\" \""+conf235[3]+"\"\n")
        fp.write(conf357[0]+" \""+conf357[1]+"\" \""+conf357[2]+"\" \""+conf357[3]+"\"\n")
        fp.write(conf245[0]+" \""+conf245[1]+"\" \""+conf245[2]+"\" \""+conf245[3]+"\"\n")
        fp.write(conf226[0]+" \""+conf226[1]+"\" \""+conf226[2]+"\" \""+conf226[3]+"\"\n")
        fp.write(conf236[0]+" \""+conf236[1]+"\" \""+conf236[2]+"\" \""+conf236[3]+"\"\n")
        fp.write(conf225[0]+" \""+conf225[1]+"\" \""+conf225[2]+"\" \""+conf225[3]+"\"\n")
        fp.write(conf358[0]+" \""+conf358[1]+"\" \""+conf358[2]+"\" \""+conf358[3]+"\"\n")
        fp.write(conf359[0]+" \""+conf359[1]+"\" \""+conf359[2]+"\" \""+conf359[3]+"\"\n")
        fp.write(conf360[0]+" \""+conf360[1]+"\" \""+conf360[2]+"\" \""+conf360[3]+"\"\n")
        fp.write(conf356[0]+" \""+conf356[1]+"\" \""+conf356[2]+"\" \""+conf356[3]+"\"\n")
        fp.write(conf264[0]+" \""+conf264[1]+"\" \""+conf264[2]+"\" \""+conf264[3]+"\"\n")
        fp.close()
        os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)