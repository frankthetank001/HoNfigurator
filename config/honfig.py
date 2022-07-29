import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import stat
from os.path import exists

class honfig():
    def __init__(self):
        self.conf1=["SetSave","_testTrialAccount","false","0"]
        self.conf2=["SetSave","cam_alwaysThirdPerson","false","0"]
        self.conf3=["SetSave","cam_fov","90.0000","0"]
        self.conf4=["SetSave","cam_smoothAnglesHalfLife","0.0500","0"]
        self.conf5=["SetSave","cam_smoothPositionHalfLife","0.1000","0"]
        self.conf6=["SetSave","cc_curGameChannel","","0"]
        self.conf7=["SetSave","cc_DisableNotifications","false","0"]
        self.conf8=["SetSave","cc_DisableNotificationsInGame","false","0"]
        self.conf9=["SetSave","cc_notificationDuration","10","0"]
        self.conf10=["SetSave","cc_showBuddyAddNotification","true","0"]
        self.conf11=["SetSave","cc_showBuddyConnectionNotification","true","0"]
        self.conf12=["SetSave","cc_showBuddyDisconnectionNotification","true","0"]
        self.conf13=["SetSave","cc_showBuddyJoinGameNotification","true","0"]
        self.conf14=["SetSave","cc_showBuddyLeaveGameNotification","true","0"]
        self.conf15=["SetSave","cc_showBuddyRemovedNotification","true","0"]
        self.conf16=["SetSave","cc_showBuddyRequestNotification","true","0"]
        self.conf17=["SetSave","cc_showClanAddNotification","true","0"]
        self.conf18=["SetSave","cc_showClanConnectionNotification","true","0"]
        self.conf19=["SetSave","cc_showClanDisconnectionNotification","true","0"]
        self.conf20=["SetSave","cc_showClanJoinGameNotification","true","0"]
        self.conf21=["SetSave","cc_showClanLeaveGameNotification","true","0"]
        self.conf22=["SetSave","cc_showClanMessageNotification","true","0"]
        self.conf23=["SetSave","cc_showClanRankNotification","true","0"]
        self.conf24=["SetSave","cc_showClanRemoveNotification","true","0"]
        self.conf25=["SetSave","cc_showGameInvites","true","0"]
        self.conf26=["SetSave","cc_showIMNotification","true","0"]
        self.conf27=["SetSave","cc_showNewPatchNotification","true","0"]
        self.conf28=["SetSave","cc_TMMMatchFidelity","0","0"]
        self.conf29=["SetSave","cg_censorChat","true","0"]
        self.conf30=["SetSave","cg_disableReleasedShaderCache","false","0"]
        self.conf31=["SetSave","cg_healthLerpMode","2","0"]
        self.conf32=["SetSave","cg_healthLerpMode2MaxMultipler","4","0"]
        self.conf33=["SetSave","cg_healthLerpMode2Multipler","0.3330","0"]
        self.conf34=["SetSave","cg_muteAnnouncerVoice","false","0"]
        self.conf35=["SetSave","chat_connectTimeout","3","0"]
        self.conf36=["SetSave","chat_gameLobbyChatToggle","274","0"]
        self.conf37=["SetSave","chat_maxReconnectAttempts","5","0"]
        self.conf38=["SetSave","chat_showChatTimestamps","false","0"]
        self.conf39=["SetSave","cl_connectionID","0","0"]
        self.conf40=["SetSave","cl_infoRequestRate","30.0000","0"]
        self.conf41=["SetSave","cl_packetSendFPS","30","0"]
        self.conf42=["SetSave","cl_printStateStringChanges","false","0"]
        self.conf43=["SetSave","cl_Rap2Enable","false","0"]
        self.conf44=["SetSave","con_alpha","1.0000","0"]
        self.conf45=["SetSave","con_bgColor","0.5000,0.5000,0.5000","0"]
        self.conf46=["SetSave","con_color","1.0000,1.0000,1.0000","0"]
        self.conf47=["SetSave","con_font","system_medium","0"]
        self.conf48=["SetSave","con_height","1.0000","0"]
        self.conf49=["SetSave","con_notify","false","0"]
        self.conf50=["SetSave","con_notifyLines","8","0"]
        self.conf51=["SetSave","con_notifyTime","4000","0"]
        self.conf52=["SetSave","con_prompt",">","0"]
        self.conf53=["SetSave","con_tabWidth","5","0"]
        self.conf54=["SetSave","con_terminalOut","false","0"]
        self.conf55=["SetSave","con_toggleTime","200","0"]
        self.conf56=["SetSave","con_wordWrap","false","0"]
        self.conf57=["SetSave","cow_precache","false","0"]
        self.conf58=["SetSave","d3d_altCursor","false","0"]
        self.conf59=["SetSave","d3d_exclusive","true","0"]
        self.conf60=["SetSave","d3d_flush","1","0"]
        self.conf61=["SetSave","d3d_hardwareRaster","true","0"]
        self.conf62=["SetSave","d3d_hardwareTL","true","0"]
        self.conf63=["SetSave","d3d_modeExNew","true","0"]
        self.conf64=["SetSave","d3d_presentInterval","0","0"]
        self.conf65=["SetSave","d3d_pure","true","0"]
        self.conf66=["SetSave","d3d_software","false","0"]
        self.conf67=["SetSave","d3d_tripleBuffering","false","0"]
        self.conf68=["SetSave","d_debugRendererFont","system_medium","0"]
        self.conf69=["SetSave","d_debugRendererModel","/core/null/null.mdf","0"]
        self.conf70=["SetSave","fs_disablemods","false","0"]
        self.conf71=["SetSave","gfx_depthFirst","false","0"]
        self.conf72=["SetSave","gfx_foliage","true","0"]
        self.conf73=["SetSave","gfx_sky","false","0"]
        self.conf74=["SetSave","gui_colorscale1_1","1.6000,1.8000,1.7000,1.0000","0"]
        self.conf75=["SetSave","host_affinity","0","0"]
        self.conf76=["SetSave","host_backuplanguage","en","0"]
        self.conf77=["SetSave","host_benchmarkControlsProfiling","false","0"]
        self.conf78=["SetSave","host_cloudAutoDownload","false","0"]
        self.conf79=["SetSave","host_cloudAutoUpload","false","0"]
        self.conf80=["SetSave","host_cloudLastModified","","0"]
        self.conf81=["SetSave","host_cloudLastModifiedUser","","0"]
        self.conf82=["SetSave","host_debugInit","false","0"]
        self.conf83=["SetSave","host_dnsResolveFrequency","60000","0"]
        self.conf84=["SetSave","host_dynamicResReload","false","0"]
        self.conf85=["SetSave","host_language","en","0"]
        self.conf86=["SetSave","host_maximumFPS","240","0"]
        self.conf87=["SetSave","host_resReloadDelay","1","0"]
        self.conf88=["SetSave","host_runOnce","","0"]
        self.conf89=["SetSave","host_screenshotFormat","jpg","0"]
        self.conf90=["SetSave","host_screenshotQuality","90","0"]
        self.conf91=["SetSave","host_vidDriver","vid_d3d9","0"]
        self.conf92=["SetSave","http_defaultConnectTimeout","15","0"]
        self.conf93=["SetSave","http_defaultLowSpeedLimit","10","0"]
        self.conf94=["SetSave","http_defaultLowSpeedTimeout","25","0"]
        self.conf95=["SetSave","http_defaultTimeout","30","0"]
        self.conf96=["SetSave","http_printDebugInfo","false","0"]
        self.conf97=["SetSave","http_upload_tunnel_count","1","0"]
        self.conf98=["SetSave","http_useCompression","true","0"]
        self.conf99=["SetSave","input_joyControlCursor","false","0"]
        self.conf100=["SetSave","input_joyCursorSpeed","150.0000","0"]
        self.conf101=["SetSave","input_joyCursorX","3","0"]
        self.conf102=["SetSave","input_joyCursorY","4","0"]
        self.conf103=["SetSave","input_joyDeadZoneR","0.1000","0"]
        self.conf104=["SetSave","input_joyDeadZoneU","0.1000","0"]
        self.conf105=["SetSave","input_joyDeadZoneV","0.1000","0"]
        self.conf106=["SetSave","input_joyDeadZoneX","0.1000","0"]
        self.conf107=["SetSave","input_joyDeadZoneY","0.1000","0"]
        self.conf108=["SetSave","input_joyDeadZoneZ","0.1000","0"]
        self.conf109=["SetSave","input_joyDeviceID","-1","0"]
        self.conf110=["SetSave","input_joyGainR","1.0000","0"]
        self.conf111=["SetSave","input_joyGainU","1.0000","0"]
        self.conf112=["SetSave","input_joyGainV","1.0000","0"]
        self.conf113=["SetSave","input_joyGainX","1.0000","0"]
        self.conf114=["SetSave","input_joyGainY","1.0000","0"]
        self.conf115=["SetSave","input_joyGainZ","1.0000","0"]
        self.conf116=["SetSave","input_joyInvertR","false","0"]
        self.conf117=["SetSave","input_joyInvertU","false","0"]
        self.conf118=["SetSave","input_joyInvertV","false","0"]
        self.conf119=["SetSave","input_joyInvertX","false","0"]
        self.conf120=["SetSave","input_joyInvertY","false","0"]
        self.conf121=["SetSave","input_joyInvertZ","false","0"]
        self.conf122=["SetSave","input_joySensitivityR","1.0000","0"]
        self.conf123=["SetSave","input_joySensitivityU","1.0000","0"]
        self.conf124=["SetSave","input_joySensitivityV","1.0000","0"]
        self.conf125=["SetSave","input_joySensitivityX","1.0000","0"]
        self.conf126=["SetSave","input_joySensitivityY","1.0000","0"]
        self.conf127=["SetSave","input_joySensitivityZ","1.0000","0"]
        self.conf128=["SetSave","input_mouseInvertX","false","0"]
        self.conf129=["SetSave","input_mouseInvertY","false","0"]
        self.conf130=["SetSave","input_mouseSensitivity","1.0000","0"]
        self.conf131=["SetSave","input_mouseSensitivityX","1.0000","0"]
        self.conf132=["SetSave","input_mouseSensitivityY","1.0000","0"]
        self.conf133=["SetSave","key_splitAlt","false","0"]
        self.conf134=["SetSave","key_splitCtrl","false","0"]
        self.conf135=["SetSave","key_splitEnter","false","0"]
        self.conf136=["SetSave","key_splitShift","false","0"]
        self.conf137=["SetSave","key_splitWin","false","0"]
        self.conf138=["SetSave","login_invisible","false","0"]
        self.conf139=["SetSave","man_allowCPUs","","0"]
        self.conf140=["SetSave","man_autoServersPerCPU","0","0"]
        self.conf141=["SetSave","man_broadcastSlaves","true","0"]
        self.conf142=["SetSave","man_cowServerPort","10234","0"]
        self.conf143=["SetSave","man_cowVoiceProxyPort","10434","0"]
        self.conf144=["SetSave","man_enableProxy","true","0"]
        self.conf145=["SetSave","man_endServerPort","10335","0"]
        self.conf146=["SetSave","man_idleTarget","1","0"]
        self.conf147=["SetSave","man_logPeriod","5000","0"]
        self.conf148=["SetSave","man_logUploadInterval","60","0"]
        self.conf149=["SetSave","man_masterLogin","","0"]
        self.conf150=["SetSave","man_masterPassword","","0"]
        self.conf151=["SetSave","man_maxServers","-1","0"]
        self.conf152=["SetSave","man_numSlaveAccounts","10","0"]
        self.conf153=["SetSave","man_port","1035","0"]
        self.conf154=["SetSave","man_resetOnCowError","true","0"]
        self.conf155=["SetSave","man_resubmitStats","true","0"]
        self.conf156=["SetSave","man_startServerPort","10235","0"]
        self.conf157=["SetSave","man_uploadReplays","true","0"]
        self.conf158=["SetSave","man_voiceProxyEndPort","10535","0"]
        self.conf159=["SetSave","man_voiceProxyStartPort","10435","0"]
        self.conf160=["SetSave","mem_font","system_medium","0"]
        self.conf161=["SetSave","model_quality","high","0"]
        self.conf162=["SetSave","net_FPS","20","0"]
        self.conf163=["SetSave","net_maxBPS","20000","0"]
        self.conf164=["SetSave","net_maxPacketSize","1300","0"]
        self.conf165=["SetSave","prof_font","system_medium","0"]
        self.conf166=["SetSave","sample_frontLoadSound","true","0"]
        self.conf167=["SetSave","scene_entityDrawDistance","6500.0000","0"]
        self.conf168=["SetSave","scene_farClip","3000.0000","0"]
        self.conf169=["SetSave","scene_farClipCalcDebug","false","0"]
        self.conf170=["SetSave","scene_foliageDrawDistance","3000.0000","0"]
        self.conf171=["SetSave","scene_rimAlpha","0.5000,0.5000,0.5000","0"]
        self.conf172=["SetSave","sound_bufferSize","-1","0"]
        self.conf173=["SetSave","sound_disable","false","0"]
        self.conf174=["SetSave","sound_disableRecording","false","0"]
        self.conf175=["SetSave","sound_driver","0","0"]
        self.conf176=["SetSave","sound_interfaceVolume","0.7000","0"]
        self.conf177=["SetSave","sound_masterVolume","1.0000","0"]
        self.conf178=["SetSave","sound_maxVariations","16","0"]
        self.conf179=["SetSave","sound_mixrate","44100","0"]
        self.conf180=["SetSave","sound_mono","false","0"]
        self.conf181=["SetSave","sound_monoBoost","1.0000","0"]
        self.conf182=["SetSave","sound_monoToStereoVolume","0.8000","0"]
        self.conf183=["SetSave","sound_musicVolume","0.2000","0"]
        self.conf184=["SetSave","sound_mute","false","0"]
        self.conf185=["SetSave","sound_muteMusic","false","0"]
        self.conf186=["SetSave","sound_numChannels","128","0"]
        self.conf187=["SetSave","sound_output","","0"]
        self.conf188=["SetSave","sound_pitchShift","true","0"]
        self.conf189=["SetSave","sound_prologic","false","0"]
        self.conf190=["SetSave","sound_recording_driver","0","0"]
        self.conf191=["SetSave","sound_resampler","2","0"]
        self.conf192=["SetSave","sound_sfxVolume","0.6000","0"]
        self.conf193=["SetSave","sound_speakerModeMono","false","0"]
        self.conf194=["SetSave","sound_speakerModeStereo","true","0"]
        self.conf195=["SetSave","sound_stereo","false","0"]
        self.conf196=["SetSave","sound_stereoBoost","1.0000","0"]
        self.conf197=["SetSave","sound_updateFrameFrequncyMs","5000","0"]
        self.conf198=["SetSave","sound_useCompressedSamples","true","0"]
        self.conf199=["SetSave","sound_voiceChatVolume","1.0000","0"]
        self.conf200=["SetSave","sound_voiceMicMuted","false","0"]
        self.conf201=["SetSave","sv_logcollection_highping_interval","120000","0"]
        self.conf202=["SetSave","sv_logcollection_highping_reportclientnum","1","0"]
        self.conf203=["SetSave","sv_logcollection_highping_value","100","0"]
        self.conf204=["SetSave","sv_remoteAdmins","","0"]
        self.conf205=["SetSave","svr_adminPassword","","0"]
        self.conf206=["SetSave","svr_authTimeout","10000","0"]
        self.conf207=["SetSave","svr_broadcast","false","0"]
        self.conf208=["SetSave","svr_chatConnectedTimeout","30000","0"]
        self.conf209=["SetSave","svr_chatConnectTimeout","10000","0"]
        self.conf210=["SetSave","svr_chatReconnectDelay","15000","0"]
        self.conf211=["SetSave","svr_clientConnectedTimeout","30000","0"]
        self.conf212=["SetSave","svr_clientConnectingTimeout","30000","0"]
        self.conf213=["SetSave","svr_clientRefreshUpgradesThrottle","5000","0"]
        self.conf214=["SetSave","svr_clientReminderInterval","5000","0"]
        self.conf215=["SetSave","svr_clientWarnTimeout","2000","0"]
        self.conf216=["SetSave","svr_connectReqPeriod","3000","0"]
        self.conf217=["SetSave","svr_connectReqThreshold","10","0"]
        self.conf218=["SetSave","svr_desc","","0"]
        self.conf219=["SetSave","svr_diagnosticsInterval","5000","0"]
        self.conf220=["SetSave","svr_firstSnapshotRetryInterval","5000","0"]
        self.conf221=["SetSave","svr_gameFPS","20","0"]
        self.conf222=["SetSave","svr_heartbeatInterval","60000","0"]
        self.conf223=["SetSave","svr_ip","","0"]
        self.conf224=["SetSave","svr_kickBanCount","2","0"]
        self.conf225=["SetSave","svr_location","","0"]
        self.conf226=["SetSave","svr_login","","0"]
        self.conf227=["SetSave","svr_longFrameWarnTime","125","0"]
        self.conf228=["SetSave","svr_masterServerAuthScript","/server_requester.php","0"]
        self.conf229=["SetSave","svr_maxbps","20000","0"]
        self.conf230=["SetSave","svr_maxClients","-1","0"]
        self.conf231=["SetSave","svr_maxFramesPerHostFrame","2","0"]
        self.conf232=["SetSave","svr_maxReminders","5","0"]
        self.conf233=["SetSave","svr_minSnapshotCompressSize","256","0"]
        self.conf234=["SetSave","svr_minStateStringCompressSize","256","0"]
        self.conf235=["SetSave","svr_name","Configure Me","0"]
        self.conf236=["SetSave","svr_password","","0"]
        self.conf237=["SetSave","svr_port","10235","0"]
        self.conf238=["SetSave","svr_proxyLocalVoicePort","10435","0"]
        self.conf239=["SetSave","svr_proxyPort","11235","0"]
        self.conf240=["SetSave","svr_proxyRemoteVoicePort","20435","0"]
        self.conf241=["SetSave","svr_reliableUnresponsiveTime","1500","0"]
        self.conf242=["SetSave","svr_replaysegment_package_size","2","0"]
        self.conf243=["SetSave","svr_replaysegment_pressure","1","0"]
        self.conf244=["SetSave","svr_requestSessionCookieTimeout","10000","0"]
        self.conf245=["SetSave","svr_requireAuthentication","true","0"]
        self.conf246=["SetSave","svr_showLongServerFrames","true","0"]
        self.conf247=["SetSave","svr_snapshotCompress","false","0"]
        self.conf248=["SetSave","svr_stateStringCompress","true","0"]
        self.conf249=["SetSave","svr_submitStats","true","0"]
        self.conf250=["SetSave","svr_userPassword","","0"]
        self.conf251=["SetSave","svr_voicePortEnd","10535","0"]
        self.conf252=["SetSave","svr_voicePortStart","10435","0"]
        self.conf253=["SetSave","sys_autoSaveConfig","true","0"]
        self.conf254=["SetSave","sys_autoSaveDump","false","0"]
        self.conf255=["SetSave","sys_dedicatedServerCrashReport","false","0"]
        self.conf256=["SetSave","sys_keepDumpAfterUpload","true","1"]
        self.conf257=["SetSave","sys_keepOldDumpsOnStartup","false","0"]
        self.conf258=["SetSave","ui_drawGrid","false","0"]
        self.conf259=["SetSave","ui_modelPanelCursorRotAnglePerPixel","0.5000","0"]
        self.conf260=["SetSave","ui_modelPanelCursorRotTime","200","0"]
        self.conf261=["SetSave","ui_translateLabels","true","0"]
        self.conf262=["SetSave","ui_webPanelDebug","false","0"]
        self.conf263=["SetSave","ui_widgetTreeFont","system_medium","0"]
        self.conf264=["SetSave","upd_checkForUpdates","false","0"]
        self.conf265=["SetSave","upd_ftpActive","false","0"]
        self.conf266=["SetSave","upd_maxActiveDownloads","6","0"]
        self.conf267=["SetSave","vid_alphaTestRef","90","0"]
        self.conf268=["SetSave","vid_antialiasing","0,0","0"]
        self.conf269=["SetSave","vid_aspect","","0"]
        self.conf270=["SetSave","vid_bpp","32","0"]
        self.conf271=["SetSave","vid_chameleonEnviromentCopy","false","0"]
        self.conf272=["SetSave","vid_chameleonNumPixelLookUps","50","0"]
        self.conf273=["SetSave","vid_chameleonSaturationMax","1.0000","0"]
        self.conf274=["SetSave","vid_chameleonSaturationMin","0.0000","0"]
        self.conf275=["SetSave","vid_chameleonValueMax","1.0000","0"]
        self.conf276=["SetSave","vid_chameleonValueMin","0.5000","0"]
        self.conf277=["SetSave","vid_cullGroundSprites","true","0"]
        self.conf278=["SetSave","vid_cullGroundSpritesSize","5000.0000","0"]
        self.conf279=["SetSave","vid_dynamicLights","true","0"]
        self.conf280=["SetSave","vid_enableGuiChannels","true","0"]
        self.conf281=["SetSave","vid_foliageAlphaTestRef","90","0"]
        self.conf282=["SetSave","vid_foliageAlphaTestRef2","90","0"]
        self.conf283=["SetSave","vid_foliageDensity","1.0000","0"]
        self.conf284=["SetSave","vid_foliageFalloffDistance","100.0000","0"]
        self.conf285=["SetSave","vid_foliageMinDensity","0.0000","0"]
        self.conf286=["SetSave","vid_foliageMinHeight","20.0000","0"]
        self.conf287=["SetSave","vid_foliageMinScale","0.2500","0"]
        self.conf288=["SetSave","vid_foliageMinWidth","5.0000","0"]
        self.conf289=["SetSave","vid_foliageRenderType","0","0"]
        self.conf290=["SetSave","vid_fullscreen","true","0"]
        self.conf291=["SetSave","vid_gamma","1.1000","0"]
        self.conf292=["SetSave","vid_geometryPreload","true","0"]
        self.conf293=["SetSave","vid_lodBias","0","0"]
        self.conf294=["SetSave","vid_lodCurve","2","0"]
        self.conf295=["SetSave","vid_lodForce","-1","0"]
        self.conf296=["SetSave","vid_lodUse","true","0"]
        self.conf297=["SetSave","vid_maxDynamicLights","4","0"]
        self.conf298=["SetSave","vid_meshForceNonBlendedDeform","false","0"]
        self.conf299=["SetSave","vid_meshGPUDeform","true","0"]
        self.conf300=["SetSave","vid_motionBlur","false","0"]
        self.conf301=["SetSave","vid_outlines","true","0"]
        self.conf302=["SetSave","vid_postEffectMipmaps","true","0"]
        self.conf303=["SetSave","vid_postEffects","true","0"]
        self.conf304=["SetSave","vid_precreateDynamicBuffers","false","0"]
        self.conf305=["SetSave","vid_reflectionMapSize","1","0"]
        self.conf306=["SetSave","vid_reflections","false","0"]
        self.conf307=["SetSave","vid_refreshRate","32","0"]
        self.conf308=["SetSave","vid_resolution","2560,1080","0"]
        self.conf309=["SetSave","vid_sceneBuffer","true","0"]
        self.conf310=["SetSave","vid_sceneBufferMipmap","true","0"]
        self.conf311=["SetSave","vid_shader_Precache","true","0"]
        self.conf312=["SetSave","vid_shaderCRC","true","0"]
        self.conf313=["SetSave","vid_shaderDebug","false","0"]
        self.conf314=["SetSave","vid_shaderFalloffQuality","0","0"]
        self.conf315=["SetSave","vid_shaderFogQuality","0","0"]
        self.conf316=["SetSave","vid_shaderLegacyCompiler","false","0"]
        self.conf317=["SetSave","vid_shaderLightingQuality","0","0"]
        self.conf318=["SetSave","vid_shaderPartialPrecision","false","0"]
        self.conf319=["SetSave","vid_shaderRimLighting","false","0"]
        self.conf320=["SetSave","vid_shaderSmoothSelfOcclude","true","0"]
        self.conf321=["SetSave","vid_shaderTexkill","false","0"]
        self.conf322=["SetSave","vid_shaderWaterQuality","1","0"]
        self.conf323=["SetSave","vid_shadowDrawDistance","3000.0000","0"]
        self.conf324=["SetSave","vid_shadowFalloffDistance","1000.0000","0"]
        self.conf325=["SetSave","vid_shadowLeak","0.1000","0"]
        self.conf326=["SetSave","vid_shadowmapFilterWidth","1","0"]
        self.conf327=["SetSave","vid_shadowmapSize","1024","0"]
        self.conf328=["SetSave","vid_shadowmapType","1","0"]
        self.conf329=["SetSave","vid_shadows","true","0"]
        self.conf330=["SetSave","vid_specularLookup","false","0"]
        self.conf331=["SetSave","vid_terrainAlphamap","false","0"]
        self.conf332=["SetSave","vid_terrainDerepeat","false","0"]
        self.conf333=["SetSave","vid_terrainShadows","true","0"]
        self.conf334=["SetSave","vid_terrainSinglePass","true","0"]
        self.conf335=["SetSave","vid_textureAutogenMipmaps","false","0"]
        self.conf336=["SetSave","vid_textureCompression","true","0"]
        self.conf337=["SetSave","vid_textureDownsize","0","0"]
        self.conf338=["SetSave","vid_textureFiltering","2","0"]
        self.conf339=["SetSave","vid_textureMaxSize","4096","0"]
        self.conf340=["SetSave","vid_texturePreload","true","0"]
        self.conf341=["SetSave","vid_treeSmoothNormals","false","0"]
        self.conf342=["SetSave","vid_waterDisMapSize","1","0"]
        self.conf343=["SetSave","voice_audioDampen","0.4000","0"]
        self.conf344=["SetSave","voice_debug","false","0"]
        self.conf345=["SetSave","voice_disabled","false","0"]
        self.conf346=["SetSave","voice_micOnLevel","20.0000","0"]
        self.conf347=["SetSave","voice_micOnTime","1000","0"]
        self.conf348=["SetSave","voice_pushToTalk","true","0"]
        self.conf349=["SetSave","voice_volume","1.0000","0"]
        self.conf350=["SetSave","water_DirectionSmoothing","0.2500","0"]
        self.conf351=["SetSave","water_drawAboveGroundOnly","true","0"]
        self.conf352=["SetSave","water_heightDifference","10.0000","0"]
        self.conf353=["SetSave","water_smoothEdges","false","0"]
        self.conf354=["SetSave","water_smoothHeight","false","0"]
        self.conf355=["SetSave","water_smoothSamples","10","0"]
        self.conf356=["SetSave","g_perks","true","0"]
        self.conf357=["SetSave","login_useSRP","false","0"]
        self.conf358=["SetSave","svr_ignoreConnectionIDForReconnect","true","0"]
        self.conf359=["SetSave","svr_version","4.10.1","0"]
        self.conf360=["SetSave","svr_chatAddress","","0"]
        return
    def getconf1(self):
        return self.conf1	
    def getconf2(self):
        return self.conf2		
    def getconf3(self):
        return self.conf3		
    def getconf4(self):
        return self.conf4		
    def getconf5(self):
        return self.conf5		
    def getconf6(self):
        return self.conf6		
    def getconf7(self):
        return self.conf7		
    def getconf8(self):
        return self.conf8		
    def getconf9(self):
        return self.conf9		
    def getconf10(self):
        return self.conf10		
    def getconf11(self):
        return self.conf11		
    def getconf12(self):
        return self.conf12		
    def getconf13(self):
        return self.conf13		
    def getconf14(self):
        return self.conf14		
    def getconf15(self):
        return self.conf15		
    def getconf16(self):
        return self.conf16		
    def getconf17(self):
        return self.conf17		
    def getconf18(self):
        return self.conf18		
    def getconf19(self):
        return self.conf19		
    def getconf20(self):
        return self.conf20		
    def getconf21(self):
        return self.conf21		
    def getconf22(self):
        return self.conf22		
    def getconf23(self):
        return self.conf23		
    def getconf24(self):
        return self.conf24		
    def getconf25(self):
        return self.conf25		
    def getconf26(self):
        return self.conf26		
    def getconf27(self):
        return self.conf27		
    def getconf28(self):
        return self.conf28		
    def getconf29(self):
        return self.conf29		
    def getconf30(self):
        return self.conf30		
    def getconf31(self):
        return self.conf31		
    def getconf32(self):
        return self.conf32		
    def getconf33(self):
        return self.conf33		
    def getconf34(self):
        return self.conf34		
    def getconf35(self):
        return self.conf35		
    def getconf36(self):
        return self.conf36		
    def getconf37(self):
        return self.conf37		
    def getconf38(self):
        return self.conf38		
    def getconf39(self):
        return self.conf39		
    def getconf40(self):
        return self.conf40		
    def getconf41(self):
        return self.conf41		
    def getconf42(self):
        return self.conf42		
    def getconf43(self):
        return self.conf43		
    def getconf44(self):
        return self.conf44		
    def getconf45(self):
        return self.conf45		
    def getconf46(self):
        return self.conf46		
    def getconf47(self):
        return self.conf47		
    def getconf48(self):
        return self.conf48		
    def getconf49(self):
        return self.conf49		
    def getconf50(self):
        return self.conf50		
    def getconf51(self):
        return self.conf51		
    def getconf52(self):
        return self.conf52		
    def getconf53(self):
        return self.conf53		
    def getconf54(self):
        return self.conf54		
    def getconf55(self):
        return self.conf55		
    def getconf56(self):
        return self.conf56		
    def getconf57(self):
        return self.conf57		
    def getconf58(self):
        return self.conf58		
    def getconf59(self):
        return self.conf59		
    def getconf60(self):
        return self.conf60		
    def getconf61(self):
        return self.conf61		
    def getconf62(self):
        return self.conf62		
    def getconf63(self):
        return self.conf63		
    def getconf64(self):
        return self.conf64		
    def getconf65(self):
        return self.conf65		
    def getconf66(self):
        return self.conf66		
    def getconf67(self):
        return self.conf67		
    def getconf68(self):
        return self.conf68		
    def getconf69(self):
        return self.conf69		
    def getconf70(self):
        return self.conf70		
    def getconf71(self):
        return self.conf71		
    def getconf72(self):
        return self.conf72		
    def getconf73(self):
        return self.conf73		
    def getconf74(self):
        return self.conf74		
    def getconf75(self):
        return self.conf75		
    def getconf76(self):
        return self.conf76		
    def getconf77(self):
        return self.conf77		
    def getconf78(self):
        return self.conf78		
    def getconf79(self):
        return self.conf79		
    def getconf80(self):
        return self.conf80		
    def getconf81(self):
        return self.conf81		
    def getconf82(self):
        return self.conf82		
    def getconf83(self):
        return self.conf83		
    def getconf84(self):
        return self.conf84		
    def getconf85(self):
        return self.conf85		
    def getconf86(self):
        return self.conf86		
    def getconf87(self):
        return self.conf87		
    def getconf88(self):
        return self.conf88		
    def getconf89(self):
        return self.conf89		
    def getconf90(self):
        return self.conf90		
    def getconf91(self):
        return self.conf91		
    def getconf92(self):
        return self.conf92		
    def getconf93(self):
        return self.conf93		
    def getconf94(self):
        return self.conf94		
    def getconf95(self):
        return self.conf95		
    def getconf96(self):
        return self.conf96		
    def getconf97(self):
        return self.conf97		
    def getconf98(self):
        return self.conf98		
    def getconf99(self):
        return self.conf99		
    def getconf100(self):
        return self.conf100		
    def getconf101(self):
        return self.conf101		
    def getconf102(self):
        return self.conf102		
    def getconf103(self):
        return self.conf103		
    def getconf104(self):
        return self.conf104		
    def getconf105(self):
        return self.conf105		
    def getconf106(self):
        return self.conf106		
    def getconf107(self):
        return self.conf107		
    def getconf108(self):
        return self.conf108		
    def getconf109(self):
        return self.conf109		
    def getconf110(self):
        return self.conf110		
    def getconf111(self):
        return self.conf111		
    def getconf112(self):
        return self.conf112		
    def getconf113(self):
        return self.conf113		
    def getconf114(self):
        return self.conf114		
    def getconf115(self):
        return self.conf115		
    def getconf116(self):
        return self.conf116		
    def getconf117(self):
        return self.conf117		
    def getconf118(self):
        return self.conf118		
    def getconf119(self):
        return self.conf119		
    def getconf120(self):
        return self.conf120		
    def getconf121(self):
        return self.conf121		
    def getconf122(self):
        return self.conf122		
    def getconf123(self):
        return self.conf123		
    def getconf124(self):
        return self.conf124		
    def getconf125(self):
        return self.conf125		
    def getconf126(self):
        return self.conf126		
    def getconf127(self):
        return self.conf127		
    def getconf128(self):
        return self.conf128		
    def getconf129(self):
        return self.conf129		
    def getconf130(self):
        return self.conf130		
    def getconf131(self):
        return self.conf131		
    def getconf132(self):
        return self.conf132		
    def getconf133(self):
        return self.conf133		
    def getconf134(self):
        return self.conf134		
    def getconf135(self):
        return self.conf135		
    def getconf136(self):
        return self.conf136		
    def getconf137(self):
        return self.conf137		
    def getconf138(self):
        return self.conf138		
    def getconf139(self):
        return self.conf139		
    def getconf140(self):
        return self.conf140		
    def getconf141(self):
        return self.conf141		
    def getconf142(self):
        return self.conf142		
    def getconf143(self):
        return self.conf143		
    def getconf144(self):
        return self.conf144		
    def getconf145(self):
        return self.conf145		
    def getconf146(self):
        return self.conf146		
    def getconf147(self):
        return self.conf147		
    def getconf148(self):
        return self.conf148		
    def getconf149(self):
        return self.conf149		
    def getconf150(self):
        return self.conf150		
    def getconf151(self):
        return self.conf151		
    def getconf152(self):
        return self.conf152		
    def getconf153(self):
        return self.conf153		
    def getconf154(self):
        return self.conf154		
    def getconf155(self):
        return self.conf155		
    def getconf156(self):
        return self.conf156		
    def getconf157(self):
        return self.conf157		
    def getconf158(self):
        return self.conf158		
    def getconf159(self):
        return self.conf159		
    def getconf160(self):
        return self.conf160		
    def getconf161(self):
        return self.conf161		
    def getconf162(self):
        return self.conf162		
    def getconf163(self):
        return self.conf163		
    def getconf164(self):
        return self.conf164		
    def getconf165(self):
        return self.conf165		
    def getconf166(self):
        return self.conf166		
    def getconf167(self):
        return self.conf167		
    def getconf168(self):
        return self.conf168		
    def getconf169(self):
        return self.conf169		
    def getconf170(self):
        return self.conf170		
    def getconf171(self):
        return self.conf171		
    def getconf172(self):
        return self.conf172		
    def getconf173(self):
        return self.conf173		
    def getconf174(self):
        return self.conf174		
    def getconf175(self):
        return self.conf175		
    def getconf176(self):
        return self.conf176		
    def getconf177(self):
        return self.conf177		
    def getconf178(self):
        return self.conf178		
    def getconf179(self):
        return self.conf179		
    def getconf180(self):
        return self.conf180		
    def getconf181(self):
        return self.conf181		
    def getconf182(self):
        return self.conf182		
    def getconf183(self):
        return self.conf183		
    def getconf184(self):
        return self.conf184		
    def getconf185(self):
        return self.conf185		
    def getconf186(self):
        return self.conf186		
    def getconf187(self):
        return self.conf187		
    def getconf188(self):
        return self.conf188		
    def getconf189(self):
        return self.conf189		
    def getconf190(self):
        return self.conf190		
    def getconf191(self):
        return self.conf191		
    def getconf192(self):
        return self.conf192		
    def getconf193(self):
        return self.conf193		
    def getconf194(self):
        return self.conf194		
    def getconf195(self):
        return self.conf195		
    def getconf196(self):
        return self.conf196		
    def getconf197(self):
        return self.conf197		
    def getconf198(self):
        return self.conf198		
    def getconf199(self):
        return self.conf199		
    def getconf200(self):
        return self.conf200		
    def getconf201(self):
        return self.conf201		
    def getconf202(self):
        return self.conf202		
    def getconf203(self):
        return self.conf203		
    def getconf204(self):
        return self.conf204		
    def getconf205(self):
        return self.conf205		
    def getconf206(self):
        return self.conf206		
    def getconf207(self):
        return self.conf207		
    def getconf208(self):
        return self.conf208		
    def getconf209(self):
        return self.conf209		
    def getconf210(self):
        return self.conf210		
    def getconf211(self):
        return self.conf211		
    def getconf212(self):
        return self.conf212		
    def getconf213(self):
        return self.conf213		
    def getconf214(self):
        return self.conf214		
    def getconf215(self):
        return self.conf215		
    def getconf216(self):
        return self.conf216		
    def getconf217(self):
        return self.conf217		
    def getconf218(self):
        return self.conf218		
    def getconf219(self):
        return self.conf219		
    def getconf220(self):
        return self.conf220		
    def getconf221(self):
        return self.conf221		
    def getconf222(self):
        return self.conf222		
    def getconf223(self):
        return self.conf223		
    def getconf224(self):
        return self.conf224		
    def getconf225(self):
        return self.conf225		
    def getconf226(self):
        return self.conf226		
    def getconf227(self):
        return self.conf227		
    def getconf228(self):
        return self.conf228		
    def getconf229(self):
        return self.conf229		
    def getconf230(self):
        return self.conf230		
    def getconf231(self):
        return self.conf231		
    def getconf232(self):
        return self.conf232		
    def getconf233(self):
        return self.conf233		
    def getconf234(self):
        return self.conf234		
    def getconf235(self):
        return self.conf235		
    def getconf236(self):
        return self.conf236		
    def getconf237(self):
        return self.conf237		
    def getconf238(self):
        return self.conf238		
    def getconf239(self):
        return self.conf239		
    def getconf240(self):
        return self.conf240		
    def getconf241(self):
        return self.conf241		
    def getconf242(self):
        return self.conf242		
    def getconf243(self):
        return self.conf243		
    def getconf244(self):
        return self.conf244		
    def getconf245(self):
        return self.conf245		
    def getconf246(self):
        return self.conf246		
    def getconf247(self):
        return self.conf247		
    def getconf248(self):
        return self.conf248		
    def getconf249(self):
        return self.conf249		
    def getconf250(self):
        return self.conf250		
    def getconf251(self):
        return self.conf251		
    def getconf252(self):
        return self.conf252		
    def getconf253(self):
        return self.conf253		
    def getconf254(self):
        return self.conf254		
    def getconf255(self):
        return self.conf255		
    def getconf256(self):
        return self.conf256		
    def getconf257(self):
        return self.conf257		
    def getconf258(self):
        return self.conf258		
    def getconf259(self):
        return self.conf259		
    def getconf260(self):
        return self.conf260		
    def getconf261(self):
        return self.conf261		
    def getconf262(self):
        return self.conf262		
    def getconf263(self):
        return self.conf263		
    def getconf264(self):
        return self.conf264		
    def getconf265(self):
        return self.conf265		
    def getconf266(self):
        return self.conf266		
    def getconf267(self):
        return self.conf267		
    def getconf268(self):
        return self.conf268		
    def getconf269(self):
        return self.conf269		
    def getconf270(self):
        return self.conf270		
    def getconf271(self):
        return self.conf271		
    def getconf272(self):
        return self.conf272		
    def getconf273(self):
        return self.conf273		
    def getconf274(self):
        return self.conf274		
    def getconf275(self):
        return self.conf275		
    def getconf276(self):
        return self.conf276		
    def getconf277(self):
        return self.conf277		
    def getconf278(self):
        return self.conf278		
    def getconf279(self):
        return self.conf279		
    def getconf280(self):
        return self.conf280		
    def getconf281(self):
        return self.conf281		
    def getconf282(self):
        return self.conf282		
    def getconf283(self):
        return self.conf283		
    def getconf284(self):
        return self.conf284		
    def getconf285(self):
        return self.conf285		
    def getconf286(self):
        return self.conf286		
    def getconf287(self):
        return self.conf287		
    def getconf288(self):
        return self.conf288		
    def getconf289(self):
        return self.conf289		
    def getconf290(self):
        return self.conf290		
    def getconf291(self):
        return self.conf291		
    def getconf292(self):
        return self.conf292		
    def getconf293(self):
        return self.conf293		
    def getconf294(self):
        return self.conf294		
    def getconf295(self):
        return self.conf295		
    def getconf296(self):
        return self.conf296		
    def getconf297(self):
        return self.conf297		
    def getconf298(self):
        return self.conf298		
    def getconf299(self):
        return self.conf299		
    def getconf300(self):
        return self.conf300		
    def getconf301(self):
        return self.conf301		
    def getconf302(self):
        return self.conf302		
    def getconf303(self):
        return self.conf303		
    def getconf304(self):
        return self.conf304		
    def getconf305(self):
        return self.conf305		
    def getconf306(self):
        return self.conf306		
    def getconf307(self):
        return self.conf307		
    def getconf308(self):
        return self.conf308		
    def getconf309(self):
        return self.conf309		
    def getconf310(self):
        return self.conf310		
    def getconf311(self):
        return self.conf311		
    def getconf312(self):
        return self.conf312		
    def getconf313(self):
        return self.conf313		
    def getconf314(self):
        return self.conf314		
    def getconf315(self):
        return self.conf315		
    def getconf316(self):
        return self.conf316		
    def getconf317(self):
        return self.conf317		
    def getconf318(self):
        return self.conf318		
    def getconf319(self):
        return self.conf319		
    def getconf320(self):
        return self.conf320		
    def getconf321(self):
        return self.conf321		
    def getconf322(self):
        return self.conf322		
    def getconf323(self):
        return self.conf323		
    def getconf324(self):
        return self.conf324		
    def getconf325(self):
        return self.conf325		
    def getconf326(self):
        return self.conf326		
    def getconf327(self):
        return self.conf327		
    def getconf328(self):
        return self.conf328		
    def getconf329(self):
        return self.conf329		
    def getconf330(self):
        return self.conf330		
    def getconf331(self):
        return self.conf331		
    def getconf332(self):
        return self.conf332		
    def getconf333(self):
        return self.conf333		
    def getconf334(self):
        return self.conf334		
    def getconf335(self):
        return self.conf335		
    def getconf336(self):
        return self.conf336		
    def getconf337(self):
        return self.conf337		
    def getconf338(self):
        return self.conf338		
    def getconf339(self):
        return self.conf339		
    def getconf340(self):
        return self.conf340		
    def getconf341(self):
        return self.conf341		
    def getconf342(self):
        return self.conf342		
    def getconf343(self):
        return self.conf343		
    def getconf344(self):
        return self.conf344		
    def getconf345(self):
        return self.conf345		
    def getconf346(self):
        return self.conf346		
    def getconf347(self):
        return self.conf347		
    def getconf348(self):
        return self.conf348		
    def getconf349(self):
        return self.conf349		
    def getconf350(self):
        return self.conf350		
    def getconf351(self):
        return self.conf351		
    def getconf352(self):
        return self.conf352		
    def getconf353(self):
        return self.conf353		
    def getconf354(self):
        return self.conf354		
    def getconf355(self):
        return self.conf355
    def getconf356(self):
        return self.conf356
    def getconf356(self):
        return self.conf357
    def getconf356(self):
        return self.conf358
    def getconf356(self):
        return self.conf359
    def getconf356(self):
        return self.conf360
    def setconf1(self, id, value):
        self.conf1[id]=value
    def setconf2(self, id, value):
        self.conf2[id]=value
    def setconf3(self, id, value):
        self.conf3[id]=value
    def setconf4(self, id, value):
        self.conf4[id]=value
    def setconf5(self, id, value):
        self.conf5[id]=value
    def setconf6(self, id, value):
        self.conf6[id]=value
    def setconf7(self, id, value):
        self.conf7[id]=value
    def setconf8(self, id, value):
        self.conf8[id]=value
    def setconf9(self, id, value):
        self.conf9[id]=value
    def setconf10(self, id, value):
        self.conf10[id]=value
    def setconf11(self, id, value):
        self.conf11[id]=value
    def setconf12(self, id, value):
        self.conf12[id]=value
    def setconf13(self, id, value):
        self.conf13[id]=value
    def setconf14(self, id, value):
        self.conf14[id]=value
    def setconf15(self, id, value):
        self.conf15[id]=value
    def setconf16(self, id, value):
        self.conf16[id]=value
    def setconf17(self, id, value):
        self.conf17[id]=value
    def setconf18(self, id, value):
        self.conf18[id]=value
    def setconf19(self, id, value):
        self.conf19[id]=value
    def setconf20(self, id, value):
        self.conf20[id]=value
    def setconf21(self, id, value):
        self.conf21[id]=value
    def setconf22(self, id, value):
        self.conf22[id]=value
    def setconf23(self, id, value):
        self.conf23[id]=value
    def setconf24(self, id, value):
        self.conf24[id]=value
    def setconf25(self, id, value):
        self.conf25[id]=value
    def setconf26(self, id, value):
        self.conf26[id]=value
    def setconf27(self, id, value):
        self.conf27[id]=value
    def setconf28(self, id, value):
        self.conf28[id]=value
    def setconf29(self, id, value):
        self.conf29[id]=value
    def setconf30(self, id, value):
        self.conf30[id]=value
    def setconf31(self, id, value):
        self.conf31[id]=value
    def setconf32(self, id, value):
        self.conf32[id]=value
    def setconf33(self, id, value):
        self.conf33[id]=value
    def setconf34(self, id, value):
        self.conf34[id]=value
    def setconf35(self, id, value):
        self.conf35[id]=value
    def setconf36(self, id, value):
        self.conf36[id]=value
    def setconf37(self, id, value):
        self.conf37[id]=value
    def setconf38(self, id, value):
        self.conf38[id]=value
    def setconf39(self, id, value):
        self.conf39[id]=value
    def setconf40(self, id, value):
        self.conf40[id]=value
    def setconf41(self, id, value):
        self.conf41[id]=value
    def setconf42(self, id, value):
        self.conf42[id]=value
    def setconf43(self, id, value):
        self.conf43[id]=value
    def setconf44(self, id, value):
        self.conf44[id]=value
    def setconf45(self, id, value):
        self.conf45[id]=value
    def setconf46(self, id, value):
        self.conf46[id]=value
    def setconf47(self, id, value):
        self.conf47[id]=value
    def setconf48(self, id, value):
        self.conf48[id]=value
    def setconf49(self, id, value):
        self.conf49[id]=value
    def setconf50(self, id, value):
        self.conf50[id]=value
    def setconf51(self, id, value):
        self.conf51[id]=value
    def setconf52(self, id, value):
        self.conf52[id]=value
    def setconf53(self, id, value):
        self.conf53[id]=value
    def setconf54(self, id, value):
        self.conf54[id]=value
    def setconf55(self, id, value):
        self.conf55[id]=value
    def setconf56(self, id, value):
        self.conf56[id]=value
    def setconf57(self, id, value):
        self.conf57[id]=value
    def setconf58(self, id, value):
        self.conf58[id]=value
    def setconf59(self, id, value):
        self.conf59[id]=value
    def setconf60(self, id, value):
        self.conf60[id]=value
    def setconf61(self, id, value):
        self.conf61[id]=value
    def setconf62(self, id, value):
        self.conf62[id]=value
    def setconf63(self, id, value):
        self.conf63[id]=value
    def setconf64(self, id, value):
        self.conf64[id]=value
    def setconf65(self, id, value):
        self.conf65[id]=value
    def setconf66(self, id, value):
        self.conf66[id]=value
    def setconf67(self, id, value):
        self.conf67[id]=value
    def setconf68(self, id, value):
        self.conf68[id]=value
    def setconf69(self, id, value):
        self.conf69[id]=value
    def setconf70(self, id, value):
        self.conf70[id]=value
    def setconf71(self, id, value):
        self.conf71[id]=value
    def setconf72(self, id, value):
        self.conf72[id]=value
    def setconf73(self, id, value):
        self.conf73[id]=value
    def setconf74(self, id, value):
        self.conf74[id]=value
    def setconf75(self, id, value):
        self.conf75[id]=value
    def setconf76(self, id, value):
        self.conf76[id]=value
    def setconf77(self, id, value):
        self.conf77[id]=value
    def setconf78(self, id, value):
        self.conf78[id]=value
    def setconf79(self, id, value):
        self.conf79[id]=value
    def setconf80(self, id, value):
        self.conf80[id]=value
    def setconf81(self, id, value):
        self.conf81[id]=value
    def setconf82(self, id, value):
        self.conf82[id]=value
    def setconf83(self, id, value):
        self.conf83[id]=value
    def setconf84(self, id, value):
        self.conf84[id]=value
    def setconf85(self, id, value):
        self.conf85[id]=value
    def setconf86(self, id, value):
        self.conf86[id]=value
    def setconf87(self, id, value):
        self.conf87[id]=value
    def setconf88(self, id, value):
        self.conf88[id]=value
    def setconf89(self, id, value):
        self.conf89[id]=value
    def setconf90(self, id, value):
        self.conf90[id]=value
    def setconf91(self, id, value):
        self.conf91[id]=value
    def setconf92(self, id, value):
        self.conf92[id]=value
    def setconf93(self, id, value):
        self.conf93[id]=value
    def setconf94(self, id, value):
        self.conf94[id]=value
    def setconf95(self, id, value):
        self.conf95[id]=value
    def setconf96(self, id, value):
        self.conf96[id]=value
    def setconf97(self, id, value):
        self.conf97[id]=value
    def setconf98(self, id, value):
        self.conf98[id]=value
    def setconf99(self, id, value):
        self.conf99[id]=value
    def setconf100(self, id, value):
        self.conf100[id]=value
    def setconf101(self, id, value):
        self.conf101[id]=value
    def setconf102(self, id, value):
        self.conf102[id]=value
    def setconf103(self, id, value):
        self.conf103[id]=value
    def setconf104(self, id, value):
        self.conf104[id]=value
    def setconf105(self, id, value):
        self.conf105[id]=value
    def setconf106(self, id, value):
        self.conf106[id]=value
    def setconf107(self, id, value):
        self.conf107[id]=value
    def setconf108(self, id, value):
        self.conf108[id]=value
    def setconf109(self, id, value):
        self.conf109[id]=value
    def setconf110(self, id, value):
        self.conf110[id]=value
    def setconf111(self, id, value):
        self.conf111[id]=value
    def setconf112(self, id, value):
        self.conf112[id]=value
    def setconf113(self, id, value):
        self.conf113[id]=value
    def setconf114(self, id, value):
        self.conf114[id]=value
    def setconf115(self, id, value):
        self.conf115[id]=value
    def setconf116(self, id, value):
        self.conf116[id]=value
    def setconf117(self, id, value):
        self.conf117[id]=value
    def setconf118(self, id, value):
        self.conf118[id]=value
    def setconf119(self, id, value):
        self.conf119[id]=value
    def setconf120(self, id, value):
        self.conf120[id]=value
    def setconf121(self, id, value):
        self.conf121[id]=value
    def setconf122(self, id, value):
        self.conf122[id]=value
    def setconf123(self, id, value):
        self.conf123[id]=value
    def setconf124(self, id, value):
        self.conf124[id]=value
    def setconf125(self, id, value):
        self.conf125[id]=value
    def setconf126(self, id, value):
        self.conf126[id]=value
    def setconf127(self, id, value):
        self.conf127[id]=value
    def setconf128(self, id, value):
        self.conf128[id]=value
    def setconf129(self, id, value):
        self.conf129[id]=value
    def setconf130(self, id, value):
        self.conf130[id]=value
    def setconf131(self, id, value):
        self.conf131[id]=value
    def setconf132(self, id, value):
        self.conf132[id]=value
    def setconf133(self, id, value):
        self.conf133[id]=value
    def setconf134(self, id, value):
        self.conf134[id]=value
    def setconf135(self, id, value):
        self.conf135[id]=value
    def setconf136(self, id, value):
        self.conf136[id]=value
    def setconf137(self, id, value):
        self.conf137[id]=value
    def setconf138(self, id, value):
        self.conf138[id]=value
    def setconf139(self, id, value):
        self.conf139[id]=value
    def setconf140(self, id, value):
        self.conf140[id]=value
    def setconf141(self, id, value):
        self.conf141[id]=value
    def setconf142(self, id, value):
        self.conf142[id]=value
    def setconf143(self, id, value):
        self.conf143[id]=value
    def setconf144(self, id, value):
        self.conf144[id]=value
    def setconf145(self, id, value):
        self.conf145[id]=value
    def setconf146(self, id, value):
        self.conf146[id]=value
    def setconf147(self, id, value):
        self.conf147[id]=value
    def setconf148(self, id, value):
        self.conf148[id]=value
    def setconf149(self, id, value):
        self.conf149[id]=value
    def setconf150(self, id, value):
        self.conf150[id]=value
    def setconf151(self, id, value):
        self.conf151[id]=value
    def setconf152(self, id, value):
        self.conf152[id]=value
    def setconf153(self, id, value):
        self.conf153[id]=value
    def setconf154(self, id, value):
        self.conf154[id]=value
    def setconf155(self, id, value):
        self.conf155[id]=value
    def setconf156(self, id, value):
        self.conf156[id]=value
    def setconf157(self, id, value):
        self.conf157[id]=value
    def setconf158(self, id, value):
        self.conf158[id]=value
    def setconf159(self, id, value):
        self.conf159[id]=value
    def setconf160(self, id, value):
        self.conf160[id]=value
    def setconf161(self, id, value):
        self.conf161[id]=value
    def setconf162(self, id, value):
        self.conf162[id]=value
    def setconf163(self, id, value):
        self.conf163[id]=value
    def setconf164(self, id, value):
        self.conf164[id]=value
    def setconf165(self, id, value):
        self.conf165[id]=value
    def setconf166(self, id, value):
        self.conf166[id]=value
    def setconf167(self, id, value):
        self.conf167[id]=value
    def setconf168(self, id, value):
        self.conf168[id]=value
    def setconf169(self, id, value):
        self.conf169[id]=value
    def setconf170(self, id, value):
        self.conf170[id]=value
    def setconf171(self, id, value):
        self.conf171[id]=value
    def setconf172(self, id, value):
        self.conf172[id]=value
    def setconf173(self, id, value):
        self.conf173[id]=value
    def setconf174(self, id, value):
        self.conf174[id]=value
    def setconf175(self, id, value):
        self.conf175[id]=value
    def setconf176(self, id, value):
        self.conf176[id]=value
    def setconf177(self, id, value):
        self.conf177[id]=value
    def setconf178(self, id, value):
        self.conf178[id]=value
    def setconf179(self, id, value):
        self.conf179[id]=value
    def setconf180(self, id, value):
        self.conf180[id]=value
    def setconf181(self, id, value):
        self.conf181[id]=value
    def setconf182(self, id, value):
        self.conf182[id]=value
    def setconf183(self, id, value):
        self.conf183[id]=value
    def setconf184(self, id, value):
        self.conf184[id]=value
    def setconf185(self, id, value):
        self.conf185[id]=value
    def setconf186(self, id, value):
        self.conf186[id]=value
    def setconf187(self, id, value):
        self.conf187[id]=value
    def setconf188(self, id, value):
        self.conf188[id]=value
    def setconf189(self, id, value):
        self.conf189[id]=value
    def setconf190(self, id, value):
        self.conf190[id]=value
    def setconf191(self, id, value):
        self.conf191[id]=value
    def setconf192(self, id, value):
        self.conf192[id]=value
    def setconf193(self, id, value):
        self.conf193[id]=value
    def setconf194(self, id, value):
        self.conf194[id]=value
    def setconf195(self, id, value):
        self.conf195[id]=value
    def setconf196(self, id, value):
        self.conf196[id]=value
    def setconf197(self, id, value):
        self.conf197[id]=value
    def setconf198(self, id, value):
        self.conf198[id]=value
    def setconf199(self, id, value):
        self.conf199[id]=value
    def setconf200(self, id, value):
        self.conf200[id]=value
    def setconf201(self, id, value):
        self.conf201[id]=value
    def setconf202(self, id, value):
        self.conf202[id]=value
    def setconf203(self, id, value):
        self.conf203[id]=value
    def setconf204(self, id, value):
        self.conf204[id]=value
    def setconf205(self, id, value):
        self.conf205[id]=value
    def setconf206(self, id, value):
        self.conf206[id]=value
    def setconf207(self, id, value):
        self.conf207[id]=value
    def setconf208(self, id, value):
        self.conf208[id]=value
    def setconf209(self, id, value):
        self.conf209[id]=value
    def setconf210(self, id, value):
        self.conf210[id]=value
    def setconf211(self, id, value):
        self.conf211[id]=value
    def setconf212(self, id, value):
        self.conf212[id]=value
    def setconf213(self, id, value):
        self.conf213[id]=value
    def setconf214(self, id, value):
        self.conf214[id]=value
    def setconf215(self, id, value):
        self.conf215[id]=value
    def setconf216(self, id, value):
        self.conf216[id]=value
    def setconf217(self, id, value):
        self.conf217[id]=value
    def setconf218(self, id, value):
        self.conf218[id]=value
    def setconf219(self, id, value):
        self.conf219[id]=value
    def setconf220(self, id, value):
        self.conf220[id]=value
    def setconf221(self, id, value):
        self.conf221[id]=value
    def setconf222(self, id, value):
        self.conf222[id]=value
    def setconf223(self, id, value):
        self.conf223[id]=value
    def setconf224(self, id, value):
        self.conf224[id]=value
    def setconf225(self, id, value):
        self.conf225[id]=value
    def setconf226(self, id, value):
        self.conf226[id]=value
    def setconf227(self, id, value):
        self.conf227[id]=value
    def setconf228(self, id, value):
        self.conf228[id]=value
    def setconf229(self, id, value):
        self.conf229[id]=value
    def setconf230(self, id, value):
        self.conf230[id]=value
    def setconf231(self, id, value):
        self.conf231[id]=value
    def setconf232(self, id, value):
        self.conf232[id]=value
    def setconf233(self, id, value):
        self.conf233[id]=value
    def setconf234(self, id, value):
        self.conf234[id]=value
    def setconf235(self, id, value):
        self.conf235[id]=value
    def setconf236(self, id, value):
        self.conf236[id]=value
    def setconf237(self, id, value):
        self.conf237[id]=value
    def setconf238(self, id, value):
        self.conf238[id]=value
    def setconf239(self, id, value):
        self.conf239[id]=value
    def setconf240(self, id, value):
        self.conf240[id]=value
    def setconf241(self, id, value):
        self.conf241[id]=value
    def setconf242(self, id, value):
        self.conf242[id]=value
    def setconf243(self, id, value):
        self.conf243[id]=value
    def setconf244(self, id, value):
        self.conf244[id]=value
    def setconf245(self, id, value):
        self.conf245[id]=value
    def setconf246(self, id, value):
        self.conf246[id]=value
    def setconf247(self, id, value):
        self.conf247[id]=value
    def setconf248(self, id, value):
        self.conf248[id]=value
    def setconf249(self, id, value):
        self.conf249[id]=value
    def setconf250(self, id, value):
        self.conf250[id]=value
    def setconf251(self, id, value):
        self.conf251[id]=value
    def setconf252(self, id, value):
        self.conf252[id]=value
    def setconf253(self, id, value):
        self.conf253[id]=value
    def setconf254(self, id, value):
        self.conf254[id]=value
    def setconf255(self, id, value):
        self.conf255[id]=value
    def setconf256(self, id, value):
        self.conf256[id]=value
    def setconf257(self, id, value):
        self.conf257[id]=value
    def setconf258(self, id, value):
        self.conf258[id]=value
    def setconf259(self, id, value):
        self.conf259[id]=value
    def setconf260(self, id, value):
        self.conf260[id]=value
    def setconf261(self, id, value):
        self.conf261[id]=value
    def setconf262(self, id, value):
        self.conf262[id]=value
    def setconf263(self, id, value):
        self.conf263[id]=value
    def setconf264(self, id, value):
        self.conf264[id]=value
    def setconf265(self, id, value):
        self.conf265[id]=value
    def setconf266(self, id, value):
        self.conf266[id]=value
    def setconf267(self, id, value):
        self.conf267[id]=value
    def setconf268(self, id, value):
        self.conf268[id]=value
    def setconf269(self, id, value):
        self.conf269[id]=value
    def setconf270(self, id, value):
        self.conf270[id]=value
    def setconf271(self, id, value):
        self.conf271[id]=value
    def setconf272(self, id, value):
        self.conf272[id]=value
    def setconf273(self, id, value):
        self.conf273[id]=value
    def setconf274(self, id, value):
        self.conf274[id]=value
    def setconf275(self, id, value):
        self.conf275[id]=value
    def setconf276(self, id, value):
        self.conf276[id]=value
    def setconf277(self, id, value):
        self.conf277[id]=value
    def setconf278(self, id, value):
        self.conf278[id]=value
    def setconf279(self, id, value):
        self.conf279[id]=value
    def setconf280(self, id, value):
        self.conf280[id]=value
    def setconf281(self, id, value):
        self.conf281[id]=value
    def setconf282(self, id, value):
        self.conf282[id]=value
    def setconf283(self, id, value):
        self.conf283[id]=value
    def setconf284(self, id, value):
        self.conf284[id]=value
    def setconf285(self, id, value):
        self.conf285[id]=value
    def setconf286(self, id, value):
        self.conf286[id]=value
    def setconf287(self, id, value):
        self.conf287[id]=value
    def setconf288(self, id, value):
        self.conf288[id]=value
    def setconf289(self, id, value):
        self.conf289[id]=value
    def setconf290(self, id, value):
        self.conf290[id]=value
    def setconf291(self, id, value):
        self.conf291[id]=value
    def setconf292(self, id, value):
        self.conf292[id]=value
    def setconf293(self, id, value):
        self.conf293[id]=value
    def setconf294(self, id, value):
        self.conf294[id]=value
    def setconf295(self, id, value):
        self.conf295[id]=value
    def setconf296(self, id, value):
        self.conf296[id]=value
    def setconf297(self, id, value):
        self.conf297[id]=value
    def setconf298(self, id, value):
        self.conf298[id]=value
    def setconf299(self, id, value):
        self.conf299[id]=value
    def setconf300(self, id, value):
        self.conf300[id]=value
    def setconf301(self, id, value):
        self.conf301[id]=value
    def setconf302(self, id, value):
        self.conf302[id]=value
    def setconf303(self, id, value):
        self.conf303[id]=value
    def setconf304(self, id, value):
        self.conf304[id]=value
    def setconf305(self, id, value):
        self.conf305[id]=value
    def setconf306(self, id, value):
        self.conf306[id]=value
    def setconf307(self, id, value):
        self.conf307[id]=value
    def setconf308(self, id, value):
        self.conf308[id]=value
    def setconf309(self, id, value):
        self.conf309[id]=value
    def setconf310(self, id, value):
        self.conf310[id]=value
    def setconf311(self, id, value):
        self.conf311[id]=value
    def setconf312(self, id, value):
        self.conf312[id]=value
    def setconf313(self, id, value):
        self.conf313[id]=value
    def setconf314(self, id, value):
        self.conf314[id]=value
    def setconf315(self, id, value):
        self.conf315[id]=value
    def setconf316(self, id, value):
        self.conf316[id]=value
    def setconf317(self, id, value):
        self.conf317[id]=value
    def setconf318(self, id, value):
        self.conf318[id]=value
    def setconf319(self, id, value):
        self.conf319[id]=value
    def setconf320(self, id, value):
        self.conf320[id]=value
    def setconf321(self, id, value):
        self.conf321[id]=value
    def setconf322(self, id, value):
        self.conf322[id]=value
    def setconf323(self, id, value):
        self.conf323[id]=value
    def setconf324(self, id, value):
        self.conf324[id]=value
    def setconf325(self, id, value):
        self.conf325[id]=value
    def setconf326(self, id, value):
        self.conf326[id]=value
    def setconf327(self, id, value):
        self.conf327[id]=value
    def setconf328(self, id, value):
        self.conf328[id]=value
    def setconf329(self, id, value):
        self.conf329[id]=value
    def setconf330(self, id, value):
        self.conf330[id]=value
    def setconf331(self, id, value):
        self.conf331[id]=value
    def setconf332(self, id, value):
        self.conf332[id]=value
    def setconf333(self, id, value):
        self.conf333[id]=value
    def setconf334(self, id, value):
        self.conf334[id]=value
    def setconf335(self, id, value):
        self.conf335[id]=value
    def setconf336(self, id, value):
        self.conf336[id]=value
    def setconf337(self, id, value):
        self.conf337[id]=value
    def setconf338(self, id, value):
        self.conf338[id]=value
    def setconf339(self, id, value):
        self.conf339[id]=value
    def setconf340(self, id, value):
        self.conf340[id]=value
    def setconf341(self, id, value):
        self.conf341[id]=value
    def setconf342(self, id, value):
        self.conf342[id]=value
    def setconf343(self, id, value):
        self.conf343[id]=value
    def setconf344(self, id, value):
        self.conf344[id]=value
    def setconf345(self, id, value):
        self.conf345[id]=value
    def setconf346(self, id, value):
        self.conf346[id]=value
    def setconf347(self, id, value):
        self.conf347[id]=value
    def setconf348(self, id, value):
        self.conf348[id]=value
    def setconf349(self, id, value):
        self.conf349[id]=value
    def setconf350(self, id, value):
        self.conf350[id]=value
    def setconf351(self, id, value):
        self.conf351[id]=value
    def setconf352(self, id, value):
        self.conf352[id]=value
    def setconf353(self, id, value):
        self.conf353[id]=value
    def setconf354(self, id, value):
        self.conf354[id]=value
    def setconf355(self, id, value):
        self.conf355[id]=value
    def setconf356(self, id, value):
        self.conf356[id]=value
    def setconf357(self, id, value):
        self.conf353[id]=value
    def setconf358(self, id, value):
        self.conf354[id]=value
    def setconf359(self, id, value):
        self.conf355[id]=value
    def setconf360(self, id, value):
        self.conf356[id]=value
    def createFile(self,file):
        if exists(file):
            os.chmod(file,stat.S_IWRITE )
        fp = open(file, 'w')
        fp.write(self.conf1[0]+" \""+self.conf1[1]+"\" \""+self.conf1[2]+"\" \""+self.conf1[3]+"\"\n")
        fp.write(self.conf2[0]+" \""+self.conf2[1]+"\" \""+self.conf2[2]+"\" \""+self.conf2[3]+"\"\n")
        fp.write(self.conf3[0]+" \""+self.conf3[1]+"\" \""+self.conf3[2]+"\" \""+self.conf3[3]+"\"\n")
        fp.write(self.conf4[0]+" \""+self.conf4[1]+"\" \""+self.conf4[2]+"\" \""+self.conf4[3]+"\"\n")
        fp.write(self.conf5[0]+" \""+self.conf5[1]+"\" \""+self.conf5[2]+"\" \""+self.conf5[3]+"\"\n")
        fp.write(self.conf6[0]+" \""+self.conf6[1]+"\" \""+self.conf6[2]+"\" \""+self.conf6[3]+"\"\n")
        fp.write(self.conf7[0]+" \""+self.conf7[1]+"\" \""+self.conf7[2]+"\" \""+self.conf7[3]+"\"\n")
        fp.write(self.conf8[0]+" \""+self.conf8[1]+"\" \""+self.conf8[2]+"\" \""+self.conf8[3]+"\"\n")
        fp.write(self.conf9[0]+" \""+self.conf9[1]+"\" \""+self.conf9[2]+"\" \""+self.conf9[3]+"\"\n")
        fp.write(self.conf10[0]+" \""+self.conf10[1]+"\" \""+self.conf10[2]+"\" \""+self.conf10[3]+"\"\n")
        fp.write(self.conf11[0]+" \""+self.conf11[1]+"\" \""+self.conf11[2]+"\" \""+self.conf11[3]+"\"\n")
        fp.write(self.conf12[0]+" \""+self.conf12[1]+"\" \""+self.conf12[2]+"\" \""+self.conf12[3]+"\"\n")
        fp.write(self.conf13[0]+" \""+self.conf13[1]+"\" \""+self.conf13[2]+"\" \""+self.conf13[3]+"\"\n")
        fp.write(self.conf14[0]+" \""+self.conf14[1]+"\" \""+self.conf14[2]+"\" \""+self.conf14[3]+"\"\n")
        fp.write(self.conf15[0]+" \""+self.conf15[1]+"\" \""+self.conf15[2]+"\" \""+self.conf15[3]+"\"\n")
        fp.write(self.conf16[0]+" \""+self.conf16[1]+"\" \""+self.conf16[2]+"\" \""+self.conf16[3]+"\"\n")
        fp.write(self.conf17[0]+" \""+self.conf17[1]+"\" \""+self.conf17[2]+"\" \""+self.conf17[3]+"\"\n")
        fp.write(self.conf18[0]+" \""+self.conf18[1]+"\" \""+self.conf18[2]+"\" \""+self.conf18[3]+"\"\n")
        fp.write(self.conf19[0]+" \""+self.conf19[1]+"\" \""+self.conf19[2]+"\" \""+self.conf19[3]+"\"\n")
        fp.write(self.conf20[0]+" \""+self.conf20[1]+"\" \""+self.conf20[2]+"\" \""+self.conf20[3]+"\"\n")
        fp.write(self.conf21[0]+" \""+self.conf21[1]+"\" \""+self.conf21[2]+"\" \""+self.conf21[3]+"\"\n")
        fp.write(self.conf22[0]+" \""+self.conf22[1]+"\" \""+self.conf22[2]+"\" \""+self.conf22[3]+"\"\n")
        fp.write(self.conf23[0]+" \""+self.conf23[1]+"\" \""+self.conf23[2]+"\" \""+self.conf23[3]+"\"\n")
        fp.write(self.conf24[0]+" \""+self.conf24[1]+"\" \""+self.conf24[2]+"\" \""+self.conf24[3]+"\"\n")
        fp.write(self.conf25[0]+" \""+self.conf25[1]+"\" \""+self.conf25[2]+"\" \""+self.conf25[3]+"\"\n")
        fp.write(self.conf26[0]+" \""+self.conf26[1]+"\" \""+self.conf26[2]+"\" \""+self.conf26[3]+"\"\n")
        fp.write(self.conf27[0]+" \""+self.conf27[1]+"\" \""+self.conf27[2]+"\" \""+self.conf27[3]+"\"\n")
        fp.write(self.conf28[0]+" \""+self.conf28[1]+"\" \""+self.conf28[2]+"\" \""+self.conf28[3]+"\"\n")
        fp.write(self.conf29[0]+" \""+self.conf29[1]+"\" \""+self.conf29[2]+"\" \""+self.conf29[3]+"\"\n")
        fp.write(self.conf30[0]+" \""+self.conf30[1]+"\" \""+self.conf30[2]+"\" \""+self.conf30[3]+"\"\n")
        fp.write(self.conf31[0]+" \""+self.conf31[1]+"\" \""+self.conf31[2]+"\" \""+self.conf31[3]+"\"\n")
        fp.write(self.conf32[0]+" \""+self.conf32[1]+"\" \""+self.conf32[2]+"\" \""+self.conf32[3]+"\"\n")
        fp.write(self.conf33[0]+" \""+self.conf33[1]+"\" \""+self.conf33[2]+"\" \""+self.conf33[3]+"\"\n")
        fp.write(self.conf34[0]+" \""+self.conf34[1]+"\" \""+self.conf34[2]+"\" \""+self.conf34[3]+"\"\n")
        fp.write(self.conf35[0]+" \""+self.conf35[1]+"\" \""+self.conf35[2]+"\" \""+self.conf35[3]+"\"\n")
        fp.write(self.conf36[0]+" \""+self.conf36[1]+"\" \""+self.conf36[2]+"\" \""+self.conf36[3]+"\"\n")
        fp.write(self.conf37[0]+" \""+self.conf37[1]+"\" \""+self.conf37[2]+"\" \""+self.conf37[3]+"\"\n")
        fp.write(self.conf38[0]+" \""+self.conf38[1]+"\" \""+self.conf38[2]+"\" \""+self.conf38[3]+"\"\n")
        fp.write(self.conf39[0]+" \""+self.conf39[1]+"\" \""+self.conf39[2]+"\" \""+self.conf39[3]+"\"\n")
        fp.write(self.conf40[0]+" \""+self.conf40[1]+"\" \""+self.conf40[2]+"\" \""+self.conf40[3]+"\"\n")
        fp.write(self.conf41[0]+" \""+self.conf41[1]+"\" \""+self.conf41[2]+"\" \""+self.conf41[3]+"\"\n")
        fp.write(self.conf42[0]+" \""+self.conf42[1]+"\" \""+self.conf42[2]+"\" \""+self.conf42[3]+"\"\n")
        fp.write(self.conf43[0]+" \""+self.conf43[1]+"\" \""+self.conf43[2]+"\" \""+self.conf43[3]+"\"\n")
        fp.write(self.conf44[0]+" \""+self.conf44[1]+"\" \""+self.conf44[2]+"\" \""+self.conf44[3]+"\"\n")
        fp.write(self.conf45[0]+" \""+self.conf45[1]+"\" \""+self.conf45[2]+"\" \""+self.conf45[3]+"\"\n")
        fp.write(self.conf46[0]+" \""+self.conf46[1]+"\" \""+self.conf46[2]+"\" \""+self.conf46[3]+"\"\n")
        fp.write(self.conf47[0]+" \""+self.conf47[1]+"\" \""+self.conf47[2]+"\" \""+self.conf47[3]+"\"\n")
        fp.write(self.conf48[0]+" \""+self.conf48[1]+"\" \""+self.conf48[2]+"\" \""+self.conf48[3]+"\"\n")
        fp.write(self.conf49[0]+" \""+self.conf49[1]+"\" \""+self.conf49[2]+"\" \""+self.conf49[3]+"\"\n")
        fp.write(self.conf50[0]+" \""+self.conf50[1]+"\" \""+self.conf50[2]+"\" \""+self.conf50[3]+"\"\n")
        fp.write(self.conf51[0]+" \""+self.conf51[1]+"\" \""+self.conf51[2]+"\" \""+self.conf51[3]+"\"\n")
        fp.write(self.conf52[0]+" \""+self.conf52[1]+"\" \""+self.conf52[2]+"\" \""+self.conf52[3]+"\"\n")
        fp.write(self.conf53[0]+" \""+self.conf53[1]+"\" \""+self.conf53[2]+"\" \""+self.conf53[3]+"\"\n")
        fp.write(self.conf54[0]+" \""+self.conf54[1]+"\" \""+self.conf54[2]+"\" \""+self.conf54[3]+"\"\n")
        fp.write(self.conf55[0]+" \""+self.conf55[1]+"\" \""+self.conf55[2]+"\" \""+self.conf55[3]+"\"\n")
        fp.write(self.conf56[0]+" \""+self.conf56[1]+"\" \""+self.conf56[2]+"\" \""+self.conf56[3]+"\"\n")
        fp.write(self.conf57[0]+" \""+self.conf57[1]+"\" \""+self.conf57[2]+"\" \""+self.conf57[3]+"\"\n")
        fp.write(self.conf58[0]+" \""+self.conf58[1]+"\" \""+self.conf58[2]+"\" \""+self.conf58[3]+"\"\n")
        fp.write(self.conf59[0]+" \""+self.conf59[1]+"\" \""+self.conf59[2]+"\" \""+self.conf59[3]+"\"\n")
        fp.write(self.conf60[0]+" \""+self.conf60[1]+"\" \""+self.conf60[2]+"\" \""+self.conf60[3]+"\"\n")
        fp.write(self.conf61[0]+" \""+self.conf61[1]+"\" \""+self.conf61[2]+"\" \""+self.conf61[3]+"\"\n")
        fp.write(self.conf62[0]+" \""+self.conf62[1]+"\" \""+self.conf62[2]+"\" \""+self.conf62[3]+"\"\n")
        fp.write(self.conf63[0]+" \""+self.conf63[1]+"\" \""+self.conf63[2]+"\" \""+self.conf63[3]+"\"\n")
        fp.write(self.conf64[0]+" \""+self.conf64[1]+"\" \""+self.conf64[2]+"\" \""+self.conf64[3]+"\"\n")
        fp.write(self.conf65[0]+" \""+self.conf65[1]+"\" \""+self.conf65[2]+"\" \""+self.conf65[3]+"\"\n")
        fp.write(self.conf66[0]+" \""+self.conf66[1]+"\" \""+self.conf66[2]+"\" \""+self.conf66[3]+"\"\n")
        fp.write(self.conf67[0]+" \""+self.conf67[1]+"\" \""+self.conf67[2]+"\" \""+self.conf67[3]+"\"\n")
        fp.write(self.conf68[0]+" \""+self.conf68[1]+"\" \""+self.conf68[2]+"\" \""+self.conf68[3]+"\"\n")
        fp.write(self.conf69[0]+" \""+self.conf69[1]+"\" \""+self.conf69[2]+"\" \""+self.conf69[3]+"\"\n")
        fp.write(self.conf70[0]+" \""+self.conf70[1]+"\" \""+self.conf70[2]+"\" \""+self.conf70[3]+"\"\n")
        fp.write(self.conf71[0]+" \""+self.conf71[1]+"\" \""+self.conf71[2]+"\" \""+self.conf71[3]+"\"\n")
        fp.write(self.conf72[0]+" \""+self.conf72[1]+"\" \""+self.conf72[2]+"\" \""+self.conf72[3]+"\"\n")
        fp.write(self.conf73[0]+" \""+self.conf73[1]+"\" \""+self.conf73[2]+"\" \""+self.conf73[3]+"\"\n")
        fp.write(self.conf74[0]+" \""+self.conf74[1]+"\" \""+self.conf74[2]+"\" \""+self.conf74[3]+"\"\n")
        fp.write(self.conf75[0]+" \""+self.conf75[1]+"\" \""+self.conf75[2]+"\" \""+self.conf75[3]+"\"\n")
        fp.write(self.conf76[0]+" \""+self.conf76[1]+"\" \""+self.conf76[2]+"\" \""+self.conf76[3]+"\"\n")
        fp.write(self.conf77[0]+" \""+self.conf77[1]+"\" \""+self.conf77[2]+"\" \""+self.conf77[3]+"\"\n")
        fp.write(self.conf78[0]+" \""+self.conf78[1]+"\" \""+self.conf78[2]+"\" \""+self.conf78[3]+"\"\n")
        fp.write(self.conf79[0]+" \""+self.conf79[1]+"\" \""+self.conf79[2]+"\" \""+self.conf79[3]+"\"\n")
        fp.write(self.conf80[0]+" \""+self.conf80[1]+"\" \""+self.conf80[2]+"\" \""+self.conf80[3]+"\"\n")
        fp.write(self.conf81[0]+" \""+self.conf81[1]+"\" \""+self.conf81[2]+"\" \""+self.conf81[3]+"\"\n")
        fp.write(self.conf82[0]+" \""+self.conf82[1]+"\" \""+self.conf82[2]+"\" \""+self.conf82[3]+"\"\n")
        fp.write(self.conf83[0]+" \""+self.conf83[1]+"\" \""+self.conf83[2]+"\" \""+self.conf83[3]+"\"\n")
        fp.write(self.conf84[0]+" \""+self.conf84[1]+"\" \""+self.conf84[2]+"\" \""+self.conf84[3]+"\"\n")
        fp.write(self.conf85[0]+" \""+self.conf85[1]+"\" \""+self.conf85[2]+"\" \""+self.conf85[3]+"\"\n")
        fp.write(self.conf86[0]+" \""+self.conf86[1]+"\" \""+self.conf86[2]+"\" \""+self.conf86[3]+"\"\n")
        fp.write(self.conf87[0]+" \""+self.conf87[1]+"\" \""+self.conf87[2]+"\" \""+self.conf87[3]+"\"\n")
        fp.write(self.conf88[0]+" \""+self.conf88[1]+"\" \""+self.conf88[2]+"\" \""+self.conf88[3]+"\"\n")
        fp.write(self.conf89[0]+" \""+self.conf89[1]+"\" \""+self.conf89[2]+"\" \""+self.conf89[3]+"\"\n")
        fp.write(self.conf90[0]+" \""+self.conf90[1]+"\" \""+self.conf90[2]+"\" \""+self.conf90[3]+"\"\n")
        fp.write(self.conf91[0]+" \""+self.conf91[1]+"\" \""+self.conf91[2]+"\" \""+self.conf91[3]+"\"\n")
        fp.write(self.conf92[0]+" \""+self.conf92[1]+"\" \""+self.conf92[2]+"\" \""+self.conf92[3]+"\"\n")
        fp.write(self.conf93[0]+" \""+self.conf93[1]+"\" \""+self.conf93[2]+"\" \""+self.conf93[3]+"\"\n")
        fp.write(self.conf94[0]+" \""+self.conf94[1]+"\" \""+self.conf94[2]+"\" \""+self.conf94[3]+"\"\n")
        fp.write(self.conf95[0]+" \""+self.conf95[1]+"\" \""+self.conf95[2]+"\" \""+self.conf95[3]+"\"\n")
        fp.write(self.conf96[0]+" \""+self.conf96[1]+"\" \""+self.conf96[2]+"\" \""+self.conf96[3]+"\"\n")
        fp.write(self.conf97[0]+" \""+self.conf97[1]+"\" \""+self.conf97[2]+"\" \""+self.conf97[3]+"\"\n")
        fp.write(self.conf98[0]+" \""+self.conf98[1]+"\" \""+self.conf98[2]+"\" \""+self.conf98[3]+"\"\n")
        fp.write(self.conf99[0]+" \""+self.conf99[1]+"\" \""+self.conf99[2]+"\" \""+self.conf99[3]+"\"\n")
        fp.write(self.conf100[0]+" \""+self.conf100[1]+"\" \""+self.conf100[2]+"\" \""+self.conf100[3]+"\"\n")
        fp.write(self.conf101[0]+" \""+self.conf101[1]+"\" \""+self.conf101[2]+"\" \""+self.conf101[3]+"\"\n")
        fp.write(self.conf102[0]+" \""+self.conf102[1]+"\" \""+self.conf102[2]+"\" \""+self.conf102[3]+"\"\n")
        fp.write(self.conf103[0]+" \""+self.conf103[1]+"\" \""+self.conf103[2]+"\" \""+self.conf103[3]+"\"\n")
        fp.write(self.conf104[0]+" \""+self.conf104[1]+"\" \""+self.conf104[2]+"\" \""+self.conf104[3]+"\"\n")
        fp.write(self.conf105[0]+" \""+self.conf105[1]+"\" \""+self.conf105[2]+"\" \""+self.conf105[3]+"\"\n")
        fp.write(self.conf106[0]+" \""+self.conf106[1]+"\" \""+self.conf106[2]+"\" \""+self.conf106[3]+"\"\n")
        fp.write(self.conf107[0]+" \""+self.conf107[1]+"\" \""+self.conf107[2]+"\" \""+self.conf107[3]+"\"\n")
        fp.write(self.conf108[0]+" \""+self.conf108[1]+"\" \""+self.conf108[2]+"\" \""+self.conf108[3]+"\"\n")
        fp.write(self.conf109[0]+" \""+self.conf109[1]+"\" \""+self.conf109[2]+"\" \""+self.conf109[3]+"\"\n")
        fp.write(self.conf110[0]+" \""+self.conf110[1]+"\" \""+self.conf110[2]+"\" \""+self.conf110[3]+"\"\n")
        fp.write(self.conf111[0]+" \""+self.conf111[1]+"\" \""+self.conf111[2]+"\" \""+self.conf111[3]+"\"\n")
        fp.write(self.conf112[0]+" \""+self.conf112[1]+"\" \""+self.conf112[2]+"\" \""+self.conf112[3]+"\"\n")
        fp.write(self.conf113[0]+" \""+self.conf113[1]+"\" \""+self.conf113[2]+"\" \""+self.conf113[3]+"\"\n")
        fp.write(self.conf114[0]+" \""+self.conf114[1]+"\" \""+self.conf114[2]+"\" \""+self.conf114[3]+"\"\n")
        fp.write(self.conf115[0]+" \""+self.conf115[1]+"\" \""+self.conf115[2]+"\" \""+self.conf115[3]+"\"\n")
        fp.write(self.conf116[0]+" \""+self.conf116[1]+"\" \""+self.conf116[2]+"\" \""+self.conf116[3]+"\"\n")
        fp.write(self.conf117[0]+" \""+self.conf117[1]+"\" \""+self.conf117[2]+"\" \""+self.conf117[3]+"\"\n")
        fp.write(self.conf118[0]+" \""+self.conf118[1]+"\" \""+self.conf118[2]+"\" \""+self.conf118[3]+"\"\n")
        fp.write(self.conf119[0]+" \""+self.conf119[1]+"\" \""+self.conf119[2]+"\" \""+self.conf119[3]+"\"\n")
        fp.write(self.conf120[0]+" \""+self.conf120[1]+"\" \""+self.conf120[2]+"\" \""+self.conf120[3]+"\"\n")
        fp.write(self.conf121[0]+" \""+self.conf121[1]+"\" \""+self.conf121[2]+"\" \""+self.conf121[3]+"\"\n")
        fp.write(self.conf122[0]+" \""+self.conf122[1]+"\" \""+self.conf122[2]+"\" \""+self.conf122[3]+"\"\n")
        fp.write(self.conf123[0]+" \""+self.conf123[1]+"\" \""+self.conf123[2]+"\" \""+self.conf123[3]+"\"\n")
        fp.write(self.conf124[0]+" \""+self.conf124[1]+"\" \""+self.conf124[2]+"\" \""+self.conf124[3]+"\"\n")
        fp.write(self.conf125[0]+" \""+self.conf125[1]+"\" \""+self.conf125[2]+"\" \""+self.conf125[3]+"\"\n")
        fp.write(self.conf126[0]+" \""+self.conf126[1]+"\" \""+self.conf126[2]+"\" \""+self.conf126[3]+"\"\n")
        fp.write(self.conf127[0]+" \""+self.conf127[1]+"\" \""+self.conf127[2]+"\" \""+self.conf127[3]+"\"\n")
        fp.write(self.conf128[0]+" \""+self.conf128[1]+"\" \""+self.conf128[2]+"\" \""+self.conf128[3]+"\"\n")
        fp.write(self.conf129[0]+" \""+self.conf129[1]+"\" \""+self.conf129[2]+"\" \""+self.conf129[3]+"\"\n")
        fp.write(self.conf130[0]+" \""+self.conf130[1]+"\" \""+self.conf130[2]+"\" \""+self.conf130[3]+"\"\n")
        fp.write(self.conf131[0]+" \""+self.conf131[1]+"\" \""+self.conf131[2]+"\" \""+self.conf131[3]+"\"\n")
        fp.write(self.conf132[0]+" \""+self.conf132[1]+"\" \""+self.conf132[2]+"\" \""+self.conf132[3]+"\"\n")
        fp.write(self.conf133[0]+" \""+self.conf133[1]+"\" \""+self.conf133[2]+"\" \""+self.conf133[3]+"\"\n")
        fp.write(self.conf134[0]+" \""+self.conf134[1]+"\" \""+self.conf134[2]+"\" \""+self.conf134[3]+"\"\n")
        fp.write(self.conf135[0]+" \""+self.conf135[1]+"\" \""+self.conf135[2]+"\" \""+self.conf135[3]+"\"\n")
        fp.write(self.conf136[0]+" \""+self.conf136[1]+"\" \""+self.conf136[2]+"\" \""+self.conf136[3]+"\"\n")
        fp.write(self.conf137[0]+" \""+self.conf137[1]+"\" \""+self.conf137[2]+"\" \""+self.conf137[3]+"\"\n")
        fp.write(self.conf138[0]+" \""+self.conf138[1]+"\" \""+self.conf138[2]+"\" \""+self.conf138[3]+"\"\n")
        fp.write(self.conf139[0]+" \""+self.conf139[1]+"\" \""+self.conf139[2]+"\" \""+self.conf139[3]+"\"\n")
        fp.write(self.conf140[0]+" \""+self.conf140[1]+"\" \""+self.conf140[2]+"\" \""+self.conf140[3]+"\"\n")
        fp.write(self.conf141[0]+" \""+self.conf141[1]+"\" \""+self.conf141[2]+"\" \""+self.conf141[3]+"\"\n")
        fp.write(self.conf142[0]+" \""+self.conf142[1]+"\" \""+self.conf142[2]+"\" \""+self.conf142[3]+"\"\n")
        fp.write(self.conf143[0]+" \""+self.conf143[1]+"\" \""+self.conf143[2]+"\" \""+self.conf143[3]+"\"\n")
        fp.write(self.conf144[0]+" \""+self.conf144[1]+"\" \""+self.conf144[2]+"\" \""+self.conf144[3]+"\"\n")
        fp.write(self.conf145[0]+" \""+self.conf145[1]+"\" \""+self.conf145[2]+"\" \""+self.conf145[3]+"\"\n")
        fp.write(self.conf146[0]+" \""+self.conf146[1]+"\" \""+self.conf146[2]+"\" \""+self.conf146[3]+"\"\n")
        fp.write(self.conf147[0]+" \""+self.conf147[1]+"\" \""+self.conf147[2]+"\" \""+self.conf147[3]+"\"\n")
        fp.write(self.conf148[0]+" \""+self.conf148[1]+"\" \""+self.conf148[2]+"\" \""+self.conf148[3]+"\"\n")
        fp.write(self.conf149[0]+" \""+self.conf149[1]+"\" \""+self.conf149[2]+"\" \""+self.conf149[3]+"\"\n")
        fp.write(self.conf150[0]+" \""+self.conf150[1]+"\" \""+self.conf150[2]+"\" \""+self.conf150[3]+"\"\n")
        fp.write(self.conf151[0]+" \""+self.conf151[1]+"\" \""+self.conf151[2]+"\" \""+self.conf151[3]+"\"\n")
        fp.write(self.conf152[0]+" \""+self.conf152[1]+"\" \""+self.conf152[2]+"\" \""+self.conf152[3]+"\"\n")
        fp.write(self.conf153[0]+" \""+self.conf153[1]+"\" \""+self.conf153[2]+"\" \""+self.conf153[3]+"\"\n")
        fp.write(self.conf154[0]+" \""+self.conf154[1]+"\" \""+self.conf154[2]+"\" \""+self.conf154[3]+"\"\n")
        fp.write(self.conf155[0]+" \""+self.conf155[1]+"\" \""+self.conf155[2]+"\" \""+self.conf155[3]+"\"\n")
        fp.write(self.conf156[0]+" \""+self.conf156[1]+"\" \""+self.conf156[2]+"\" \""+self.conf156[3]+"\"\n")
        fp.write(self.conf157[0]+" \""+self.conf157[1]+"\" \""+self.conf157[2]+"\" \""+self.conf157[3]+"\"\n")
        fp.write(self.conf158[0]+" \""+self.conf158[1]+"\" \""+self.conf158[2]+"\" \""+self.conf158[3]+"\"\n")
        fp.write(self.conf159[0]+" \""+self.conf159[1]+"\" \""+self.conf159[2]+"\" \""+self.conf159[3]+"\"\n")
        fp.write(self.conf160[0]+" \""+self.conf160[1]+"\" \""+self.conf160[2]+"\" \""+self.conf160[3]+"\"\n")
        fp.write(self.conf161[0]+" \""+self.conf161[1]+"\" \""+self.conf161[2]+"\" \""+self.conf161[3]+"\"\n")
        fp.write(self.conf162[0]+" \""+self.conf162[1]+"\" \""+self.conf162[2]+"\" \""+self.conf162[3]+"\"\n")
        fp.write(self.conf163[0]+" \""+self.conf163[1]+"\" \""+self.conf163[2]+"\" \""+self.conf163[3]+"\"\n")
        fp.write(self.conf164[0]+" \""+self.conf164[1]+"\" \""+self.conf164[2]+"\" \""+self.conf164[3]+"\"\n")
        fp.write(self.conf165[0]+" \""+self.conf165[1]+"\" \""+self.conf165[2]+"\" \""+self.conf165[3]+"\"\n")
        fp.write(self.conf166[0]+" \""+self.conf166[1]+"\" \""+self.conf166[2]+"\" \""+self.conf166[3]+"\"\n")
        fp.write(self.conf167[0]+" \""+self.conf167[1]+"\" \""+self.conf167[2]+"\" \""+self.conf167[3]+"\"\n")
        fp.write(self.conf168[0]+" \""+self.conf168[1]+"\" \""+self.conf168[2]+"\" \""+self.conf168[3]+"\"\n")
        fp.write(self.conf169[0]+" \""+self.conf169[1]+"\" \""+self.conf169[2]+"\" \""+self.conf169[3]+"\"\n")
        fp.write(self.conf170[0]+" \""+self.conf170[1]+"\" \""+self.conf170[2]+"\" \""+self.conf170[3]+"\"\n")
        fp.write(self.conf171[0]+" \""+self.conf171[1]+"\" \""+self.conf171[2]+"\" \""+self.conf171[3]+"\"\n")
        fp.write(self.conf172[0]+" \""+self.conf172[1]+"\" \""+self.conf172[2]+"\" \""+self.conf172[3]+"\"\n")
        fp.write(self.conf173[0]+" \""+self.conf173[1]+"\" \""+self.conf173[2]+"\" \""+self.conf173[3]+"\"\n")
        fp.write(self.conf174[0]+" \""+self.conf174[1]+"\" \""+self.conf174[2]+"\" \""+self.conf174[3]+"\"\n")
        fp.write(self.conf175[0]+" \""+self.conf175[1]+"\" \""+self.conf175[2]+"\" \""+self.conf175[3]+"\"\n")
        fp.write(self.conf176[0]+" \""+self.conf176[1]+"\" \""+self.conf176[2]+"\" \""+self.conf176[3]+"\"\n")
        fp.write(self.conf177[0]+" \""+self.conf177[1]+"\" \""+self.conf177[2]+"\" \""+self.conf177[3]+"\"\n")
        fp.write(self.conf178[0]+" \""+self.conf178[1]+"\" \""+self.conf178[2]+"\" \""+self.conf178[3]+"\"\n")
        fp.write(self.conf179[0]+" \""+self.conf179[1]+"\" \""+self.conf179[2]+"\" \""+self.conf179[3]+"\"\n")
        fp.write(self.conf180[0]+" \""+self.conf180[1]+"\" \""+self.conf180[2]+"\" \""+self.conf180[3]+"\"\n")
        fp.write(self.conf181[0]+" \""+self.conf181[1]+"\" \""+self.conf181[2]+"\" \""+self.conf181[3]+"\"\n")
        fp.write(self.conf182[0]+" \""+self.conf182[1]+"\" \""+self.conf182[2]+"\" \""+self.conf182[3]+"\"\n")
        fp.write(self.conf183[0]+" \""+self.conf183[1]+"\" \""+self.conf183[2]+"\" \""+self.conf183[3]+"\"\n")
        fp.write(self.conf184[0]+" \""+self.conf184[1]+"\" \""+self.conf184[2]+"\" \""+self.conf184[3]+"\"\n")
        fp.write(self.conf185[0]+" \""+self.conf185[1]+"\" \""+self.conf185[2]+"\" \""+self.conf185[3]+"\"\n")
        fp.write(self.conf186[0]+" \""+self.conf186[1]+"\" \""+self.conf186[2]+"\" \""+self.conf186[3]+"\"\n")
        fp.write(self.conf187[0]+" \""+self.conf187[1]+"\" \""+self.conf187[2]+"\" \""+self.conf187[3]+"\"\n")
        fp.write(self.conf188[0]+" \""+self.conf188[1]+"\" \""+self.conf188[2]+"\" \""+self.conf188[3]+"\"\n")
        fp.write(self.conf189[0]+" \""+self.conf189[1]+"\" \""+self.conf189[2]+"\" \""+self.conf189[3]+"\"\n")
        fp.write(self.conf190[0]+" \""+self.conf190[1]+"\" \""+self.conf190[2]+"\" \""+self.conf190[3]+"\"\n")
        fp.write(self.conf191[0]+" \""+self.conf191[1]+"\" \""+self.conf191[2]+"\" \""+self.conf191[3]+"\"\n")
        fp.write(self.conf192[0]+" \""+self.conf192[1]+"\" \""+self.conf192[2]+"\" \""+self.conf192[3]+"\"\n")
        fp.write(self.conf193[0]+" \""+self.conf193[1]+"\" \""+self.conf193[2]+"\" \""+self.conf193[3]+"\"\n")
        fp.write(self.conf194[0]+" \""+self.conf194[1]+"\" \""+self.conf194[2]+"\" \""+self.conf194[3]+"\"\n")
        fp.write(self.conf195[0]+" \""+self.conf195[1]+"\" \""+self.conf195[2]+"\" \""+self.conf195[3]+"\"\n")
        fp.write(self.conf196[0]+" \""+self.conf196[1]+"\" \""+self.conf196[2]+"\" \""+self.conf196[3]+"\"\n")
        fp.write(self.conf197[0]+" \""+self.conf197[1]+"\" \""+self.conf197[2]+"\" \""+self.conf197[3]+"\"\n")
        fp.write(self.conf198[0]+" \""+self.conf198[1]+"\" \""+self.conf198[2]+"\" \""+self.conf198[3]+"\"\n")
        fp.write(self.conf199[0]+" \""+self.conf199[1]+"\" \""+self.conf199[2]+"\" \""+self.conf199[3]+"\"\n")
        fp.write(self.conf200[0]+" \""+self.conf200[1]+"\" \""+self.conf200[2]+"\" \""+self.conf200[3]+"\"\n")
        fp.write(self.conf201[0]+" \""+self.conf201[1]+"\" \""+self.conf201[2]+"\" \""+self.conf201[3]+"\"\n")
        fp.write(self.conf202[0]+" \""+self.conf202[1]+"\" \""+self.conf202[2]+"\" \""+self.conf202[3]+"\"\n")
        fp.write(self.conf203[0]+" \""+self.conf203[1]+"\" \""+self.conf203[2]+"\" \""+self.conf203[3]+"\"\n")
        fp.write(self.conf204[0]+" \""+self.conf204[1]+"\" \""+self.conf204[2]+"\" \""+self.conf204[3]+"\"\n")
        fp.write(self.conf205[0]+" \""+self.conf205[1]+"\" \""+self.conf205[2]+"\" \""+self.conf205[3]+"\"\n")
        fp.write(self.conf206[0]+" \""+self.conf206[1]+"\" \""+self.conf206[2]+"\" \""+self.conf206[3]+"\"\n")
        fp.write(self.conf207[0]+" \""+self.conf207[1]+"\" \""+self.conf207[2]+"\" \""+self.conf207[3]+"\"\n")
        fp.write(self.conf208[0]+" \""+self.conf208[1]+"\" \""+self.conf208[2]+"\" \""+self.conf208[3]+"\"\n")
        fp.write(self.conf209[0]+" \""+self.conf209[1]+"\" \""+self.conf209[2]+"\" \""+self.conf209[3]+"\"\n")
        fp.write(self.conf210[0]+" \""+self.conf210[1]+"\" \""+self.conf210[2]+"\" \""+self.conf210[3]+"\"\n")
        fp.write(self.conf211[0]+" \""+self.conf211[1]+"\" \""+self.conf211[2]+"\" \""+self.conf211[3]+"\"\n")
        fp.write(self.conf212[0]+" \""+self.conf212[1]+"\" \""+self.conf212[2]+"\" \""+self.conf212[3]+"\"\n")
        fp.write(self.conf213[0]+" \""+self.conf213[1]+"\" \""+self.conf213[2]+"\" \""+self.conf213[3]+"\"\n")
        fp.write(self.conf214[0]+" \""+self.conf214[1]+"\" \""+self.conf214[2]+"\" \""+self.conf214[3]+"\"\n")
        fp.write(self.conf215[0]+" \""+self.conf215[1]+"\" \""+self.conf215[2]+"\" \""+self.conf215[3]+"\"\n")
        fp.write(self.conf216[0]+" \""+self.conf216[1]+"\" \""+self.conf216[2]+"\" \""+self.conf216[3]+"\"\n")
        fp.write(self.conf217[0]+" \""+self.conf217[1]+"\" \""+self.conf217[2]+"\" \""+self.conf217[3]+"\"\n")
        fp.write(self.conf218[0]+" \""+self.conf218[1]+"\" \""+self.conf218[2]+"\" \""+self.conf218[3]+"\"\n")
        fp.write(self.conf219[0]+" \""+self.conf219[1]+"\" \""+self.conf219[2]+"\" \""+self.conf219[3]+"\"\n")
        fp.write(self.conf220[0]+" \""+self.conf220[1]+"\" \""+self.conf220[2]+"\" \""+self.conf220[3]+"\"\n")
        fp.write(self.conf221[0]+" \""+self.conf221[1]+"\" \""+self.conf221[2]+"\" \""+self.conf221[3]+"\"\n")
        fp.write(self.conf222[0]+" \""+self.conf222[1]+"\" \""+self.conf222[2]+"\" \""+self.conf222[3]+"\"\n")
        fp.write(self.conf223[0]+" \""+self.conf223[1]+"\" \""+self.conf223[2]+"\" \""+self.conf223[3]+"\"\n")
        fp.write(self.conf224[0]+" \""+self.conf224[1]+"\" \""+self.conf224[2]+"\" \""+self.conf224[3]+"\"\n")
        fp.write(self.conf225[0]+" \""+self.conf225[1]+"\" \""+self.conf225[2]+"\" \""+self.conf225[3]+"\"\n")
        fp.write(self.conf226[0]+" \""+self.conf226[1]+"\" \""+self.conf226[2]+"\" \""+self.conf226[3]+"\"\n")
        fp.write(self.conf227[0]+" \""+self.conf227[1]+"\" \""+self.conf227[2]+"\" \""+self.conf227[3]+"\"\n")
        fp.write(self.conf228[0]+" \""+self.conf228[1]+"\" \""+self.conf228[2]+"\" \""+self.conf228[3]+"\"\n")
        fp.write(self.conf229[0]+" \""+self.conf229[1]+"\" \""+self.conf229[2]+"\" \""+self.conf229[3]+"\"\n")
        fp.write(self.conf230[0]+" \""+self.conf230[1]+"\" \""+self.conf230[2]+"\" \""+self.conf230[3]+"\"\n")
        fp.write(self.conf231[0]+" \""+self.conf231[1]+"\" \""+self.conf231[2]+"\" \""+self.conf231[3]+"\"\n")
        fp.write(self.conf232[0]+" \""+self.conf232[1]+"\" \""+self.conf232[2]+"\" \""+self.conf232[3]+"\"\n")
        fp.write(self.conf233[0]+" \""+self.conf233[1]+"\" \""+self.conf233[2]+"\" \""+self.conf233[3]+"\"\n")
        fp.write(self.conf234[0]+" \""+self.conf234[1]+"\" \""+self.conf234[2]+"\" \""+self.conf234[3]+"\"\n")
        fp.write(self.conf235[0]+" \""+self.conf235[1]+"\" \""+self.conf235[2]+"\" \""+self.conf235[3]+"\"\n")
        fp.write(self.conf236[0]+" \""+self.conf236[1]+"\" \""+self.conf236[2]+"\" \""+self.conf236[3]+"\"\n")
        fp.write(self.conf237[0]+" \""+self.conf237[1]+"\" \""+self.conf237[2]+"\" \""+self.conf237[3]+"\"\n")
        fp.write(self.conf238[0]+" \""+self.conf238[1]+"\" \""+self.conf238[2]+"\" \""+self.conf238[3]+"\"\n")
        fp.write(self.conf239[0]+" \""+self.conf239[1]+"\" \""+self.conf239[2]+"\" \""+self.conf239[3]+"\"\n")
        fp.write(self.conf240[0]+" \""+self.conf240[1]+"\" \""+self.conf240[2]+"\" \""+self.conf240[3]+"\"\n")
        fp.write(self.conf241[0]+" \""+self.conf241[1]+"\" \""+self.conf241[2]+"\" \""+self.conf241[3]+"\"\n")
        fp.write(self.conf242[0]+" \""+self.conf242[1]+"\" \""+self.conf242[2]+"\" \""+self.conf242[3]+"\"\n")
        fp.write(self.conf243[0]+" \""+self.conf243[1]+"\" \""+self.conf243[2]+"\" \""+self.conf243[3]+"\"\n")
        fp.write(self.conf244[0]+" \""+self.conf244[1]+"\" \""+self.conf244[2]+"\" \""+self.conf244[3]+"\"\n")
        fp.write(self.conf245[0]+" \""+self.conf245[1]+"\" \""+self.conf245[2]+"\" \""+self.conf245[3]+"\"\n")
        fp.write(self.conf246[0]+" \""+self.conf246[1]+"\" \""+self.conf246[2]+"\" \""+self.conf246[3]+"\"\n")
        fp.write(self.conf247[0]+" \""+self.conf247[1]+"\" \""+self.conf247[2]+"\" \""+self.conf247[3]+"\"\n")
        fp.write(self.conf248[0]+" \""+self.conf248[1]+"\" \""+self.conf248[2]+"\" \""+self.conf248[3]+"\"\n")
        fp.write(self.conf249[0]+" \""+self.conf249[1]+"\" \""+self.conf249[2]+"\" \""+self.conf249[3]+"\"\n")
        fp.write(self.conf250[0]+" \""+self.conf250[1]+"\" \""+self.conf250[2]+"\" \""+self.conf250[3]+"\"\n")
        fp.write(self.conf251[0]+" \""+self.conf251[1]+"\" \""+self.conf251[2]+"\" \""+self.conf251[3]+"\"\n")
        fp.write(self.conf252[0]+" \""+self.conf252[1]+"\" \""+self.conf252[2]+"\" \""+self.conf252[3]+"\"\n")
        fp.write(self.conf253[0]+" \""+self.conf253[1]+"\" \""+self.conf253[2]+"\" \""+self.conf253[3]+"\"\n")
        fp.write(self.conf254[0]+" \""+self.conf254[1]+"\" \""+self.conf254[2]+"\" \""+self.conf254[3]+"\"\n")
        fp.write(self.conf255[0]+" \""+self.conf255[1]+"\" \""+self.conf255[2]+"\" \""+self.conf255[3]+"\"\n")
        fp.write(self.conf256[0]+" \""+self.conf256[1]+"\" \""+self.conf256[2]+"\" \""+self.conf256[3]+"\"\n")
        fp.write(self.conf257[0]+" \""+self.conf257[1]+"\" \""+self.conf257[2]+"\" \""+self.conf257[3]+"\"\n")
        fp.write(self.conf258[0]+" \""+self.conf258[1]+"\" \""+self.conf258[2]+"\" \""+self.conf258[3]+"\"\n")
        fp.write(self.conf259[0]+" \""+self.conf259[1]+"\" \""+self.conf259[2]+"\" \""+self.conf259[3]+"\"\n")
        fp.write(self.conf260[0]+" \""+self.conf260[1]+"\" \""+self.conf260[2]+"\" \""+self.conf260[3]+"\"\n")
        fp.write(self.conf261[0]+" \""+self.conf261[1]+"\" \""+self.conf261[2]+"\" \""+self.conf261[3]+"\"\n")
        fp.write(self.conf262[0]+" \""+self.conf262[1]+"\" \""+self.conf262[2]+"\" \""+self.conf262[3]+"\"\n")
        fp.write(self.conf263[0]+" \""+self.conf263[1]+"\" \""+self.conf263[2]+"\" \""+self.conf263[3]+"\"\n")
        fp.write(self.conf264[0]+" \""+self.conf264[1]+"\" \""+self.conf264[2]+"\" \""+self.conf264[3]+"\"\n")
        fp.write(self.conf265[0]+" \""+self.conf265[1]+"\" \""+self.conf265[2]+"\" \""+self.conf265[3]+"\"\n")
        fp.write(self.conf266[0]+" \""+self.conf266[1]+"\" \""+self.conf266[2]+"\" \""+self.conf266[3]+"\"\n")
        fp.write(self.conf267[0]+" \""+self.conf267[1]+"\" \""+self.conf267[2]+"\" \""+self.conf267[3]+"\"\n")
        fp.write(self.conf268[0]+" \""+self.conf268[1]+"\" \""+self.conf268[2]+"\" \""+self.conf268[3]+"\"\n")
        fp.write(self.conf269[0]+" \""+self.conf269[1]+"\" \""+self.conf269[2]+"\" \""+self.conf269[3]+"\"\n")
        fp.write(self.conf270[0]+" \""+self.conf270[1]+"\" \""+self.conf270[2]+"\" \""+self.conf270[3]+"\"\n")
        fp.write(self.conf271[0]+" \""+self.conf271[1]+"\" \""+self.conf271[2]+"\" \""+self.conf271[3]+"\"\n")
        fp.write(self.conf272[0]+" \""+self.conf272[1]+"\" \""+self.conf272[2]+"\" \""+self.conf272[3]+"\"\n")
        fp.write(self.conf273[0]+" \""+self.conf273[1]+"\" \""+self.conf273[2]+"\" \""+self.conf273[3]+"\"\n")
        fp.write(self.conf274[0]+" \""+self.conf274[1]+"\" \""+self.conf274[2]+"\" \""+self.conf274[3]+"\"\n")
        fp.write(self.conf275[0]+" \""+self.conf275[1]+"\" \""+self.conf275[2]+"\" \""+self.conf275[3]+"\"\n")
        fp.write(self.conf276[0]+" \""+self.conf276[1]+"\" \""+self.conf276[2]+"\" \""+self.conf276[3]+"\"\n")
        fp.write(self.conf277[0]+" \""+self.conf277[1]+"\" \""+self.conf277[2]+"\" \""+self.conf277[3]+"\"\n")
        fp.write(self.conf278[0]+" \""+self.conf278[1]+"\" \""+self.conf278[2]+"\" \""+self.conf278[3]+"\"\n")
        fp.write(self.conf279[0]+" \""+self.conf279[1]+"\" \""+self.conf279[2]+"\" \""+self.conf279[3]+"\"\n")
        fp.write(self.conf280[0]+" \""+self.conf280[1]+"\" \""+self.conf280[2]+"\" \""+self.conf280[3]+"\"\n")
        fp.write(self.conf281[0]+" \""+self.conf281[1]+"\" \""+self.conf281[2]+"\" \""+self.conf281[3]+"\"\n")
        fp.write(self.conf282[0]+" \""+self.conf282[1]+"\" \""+self.conf282[2]+"\" \""+self.conf282[3]+"\"\n")
        fp.write(self.conf283[0]+" \""+self.conf283[1]+"\" \""+self.conf283[2]+"\" \""+self.conf283[3]+"\"\n")
        fp.write(self.conf284[0]+" \""+self.conf284[1]+"\" \""+self.conf284[2]+"\" \""+self.conf284[3]+"\"\n")
        fp.write(self.conf285[0]+" \""+self.conf285[1]+"\" \""+self.conf285[2]+"\" \""+self.conf285[3]+"\"\n")
        fp.write(self.conf286[0]+" \""+self.conf286[1]+"\" \""+self.conf286[2]+"\" \""+self.conf286[3]+"\"\n")
        fp.write(self.conf287[0]+" \""+self.conf287[1]+"\" \""+self.conf287[2]+"\" \""+self.conf287[3]+"\"\n")
        fp.write(self.conf288[0]+" \""+self.conf288[1]+"\" \""+self.conf288[2]+"\" \""+self.conf288[3]+"\"\n")
        fp.write(self.conf289[0]+" \""+self.conf289[1]+"\" \""+self.conf289[2]+"\" \""+self.conf289[3]+"\"\n")
        fp.write(self.conf290[0]+" \""+self.conf290[1]+"\" \""+self.conf290[2]+"\" \""+self.conf290[3]+"\"\n")
        fp.write(self.conf291[0]+" \""+self.conf291[1]+"\" \""+self.conf291[2]+"\" \""+self.conf291[3]+"\"\n")
        fp.write(self.conf292[0]+" \""+self.conf292[1]+"\" \""+self.conf292[2]+"\" \""+self.conf292[3]+"\"\n")
        fp.write(self.conf293[0]+" \""+self.conf293[1]+"\" \""+self.conf293[2]+"\" \""+self.conf293[3]+"\"\n")
        fp.write(self.conf294[0]+" \""+self.conf294[1]+"\" \""+self.conf294[2]+"\" \""+self.conf294[3]+"\"\n")
        fp.write(self.conf295[0]+" \""+self.conf295[1]+"\" \""+self.conf295[2]+"\" \""+self.conf295[3]+"\"\n")
        fp.write(self.conf296[0]+" \""+self.conf296[1]+"\" \""+self.conf296[2]+"\" \""+self.conf296[3]+"\"\n")
        fp.write(self.conf297[0]+" \""+self.conf297[1]+"\" \""+self.conf297[2]+"\" \""+self.conf297[3]+"\"\n")
        fp.write(self.conf298[0]+" \""+self.conf298[1]+"\" \""+self.conf298[2]+"\" \""+self.conf298[3]+"\"\n")
        fp.write(self.conf299[0]+" \""+self.conf299[1]+"\" \""+self.conf299[2]+"\" \""+self.conf299[3]+"\"\n")
        fp.write(self.conf300[0]+" \""+self.conf300[1]+"\" \""+self.conf300[2]+"\" \""+self.conf300[3]+"\"\n")
        fp.write(self.conf301[0]+" \""+self.conf301[1]+"\" \""+self.conf301[2]+"\" \""+self.conf301[3]+"\"\n")
        fp.write(self.conf302[0]+" \""+self.conf302[1]+"\" \""+self.conf302[2]+"\" \""+self.conf302[3]+"\"\n")
        fp.write(self.conf303[0]+" \""+self.conf303[1]+"\" \""+self.conf303[2]+"\" \""+self.conf303[3]+"\"\n")
        fp.write(self.conf304[0]+" \""+self.conf304[1]+"\" \""+self.conf304[2]+"\" \""+self.conf304[3]+"\"\n")
        fp.write(self.conf305[0]+" \""+self.conf305[1]+"\" \""+self.conf305[2]+"\" \""+self.conf305[3]+"\"\n")
        fp.write(self.conf306[0]+" \""+self.conf306[1]+"\" \""+self.conf306[2]+"\" \""+self.conf306[3]+"\"\n")
        fp.write(self.conf307[0]+" \""+self.conf307[1]+"\" \""+self.conf307[2]+"\" \""+self.conf307[3]+"\"\n")
        fp.write(self.conf308[0]+" \""+self.conf308[1]+"\" \""+self.conf308[2]+"\" \""+self.conf308[3]+"\"\n")
        fp.write(self.conf309[0]+" \""+self.conf309[1]+"\" \""+self.conf309[2]+"\" \""+self.conf309[3]+"\"\n")
        fp.write(self.conf310[0]+" \""+self.conf310[1]+"\" \""+self.conf310[2]+"\" \""+self.conf310[3]+"\"\n")
        fp.write(self.conf311[0]+" \""+self.conf311[1]+"\" \""+self.conf311[2]+"\" \""+self.conf311[3]+"\"\n")
        fp.write(self.conf312[0]+" \""+self.conf312[1]+"\" \""+self.conf312[2]+"\" \""+self.conf312[3]+"\"\n")
        fp.write(self.conf313[0]+" \""+self.conf313[1]+"\" \""+self.conf313[2]+"\" \""+self.conf313[3]+"\"\n")
        fp.write(self.conf314[0]+" \""+self.conf314[1]+"\" \""+self.conf314[2]+"\" \""+self.conf314[3]+"\"\n")
        fp.write(self.conf315[0]+" \""+self.conf315[1]+"\" \""+self.conf315[2]+"\" \""+self.conf315[3]+"\"\n")
        fp.write(self.conf316[0]+" \""+self.conf316[1]+"\" \""+self.conf316[2]+"\" \""+self.conf316[3]+"\"\n")
        fp.write(self.conf317[0]+" \""+self.conf317[1]+"\" \""+self.conf317[2]+"\" \""+self.conf317[3]+"\"\n")
        fp.write(self.conf318[0]+" \""+self.conf318[1]+"\" \""+self.conf318[2]+"\" \""+self.conf318[3]+"\"\n")
        fp.write(self.conf319[0]+" \""+self.conf319[1]+"\" \""+self.conf319[2]+"\" \""+self.conf319[3]+"\"\n")
        fp.write(self.conf320[0]+" \""+self.conf320[1]+"\" \""+self.conf320[2]+"\" \""+self.conf320[3]+"\"\n")
        fp.write(self.conf321[0]+" \""+self.conf321[1]+"\" \""+self.conf321[2]+"\" \""+self.conf321[3]+"\"\n")
        fp.write(self.conf322[0]+" \""+self.conf322[1]+"\" \""+self.conf322[2]+"\" \""+self.conf322[3]+"\"\n")
        fp.write(self.conf323[0]+" \""+self.conf323[1]+"\" \""+self.conf323[2]+"\" \""+self.conf323[3]+"\"\n")
        fp.write(self.conf324[0]+" \""+self.conf324[1]+"\" \""+self.conf324[2]+"\" \""+self.conf324[3]+"\"\n")
        fp.write(self.conf325[0]+" \""+self.conf325[1]+"\" \""+self.conf325[2]+"\" \""+self.conf325[3]+"\"\n")
        fp.write(self.conf326[0]+" \""+self.conf326[1]+"\" \""+self.conf326[2]+"\" \""+self.conf326[3]+"\"\n")
        fp.write(self.conf327[0]+" \""+self.conf327[1]+"\" \""+self.conf327[2]+"\" \""+self.conf327[3]+"\"\n")
        fp.write(self.conf328[0]+" \""+self.conf328[1]+"\" \""+self.conf328[2]+"\" \""+self.conf328[3]+"\"\n")
        fp.write(self.conf329[0]+" \""+self.conf329[1]+"\" \""+self.conf329[2]+"\" \""+self.conf329[3]+"\"\n")
        fp.write(self.conf330[0]+" \""+self.conf330[1]+"\" \""+self.conf330[2]+"\" \""+self.conf330[3]+"\"\n")
        fp.write(self.conf331[0]+" \""+self.conf331[1]+"\" \""+self.conf331[2]+"\" \""+self.conf331[3]+"\"\n")
        fp.write(self.conf332[0]+" \""+self.conf332[1]+"\" \""+self.conf332[2]+"\" \""+self.conf332[3]+"\"\n")
        fp.write(self.conf333[0]+" \""+self.conf333[1]+"\" \""+self.conf333[2]+"\" \""+self.conf333[3]+"\"\n")
        fp.write(self.conf334[0]+" \""+self.conf334[1]+"\" \""+self.conf334[2]+"\" \""+self.conf334[3]+"\"\n")
        fp.write(self.conf335[0]+" \""+self.conf335[1]+"\" \""+self.conf335[2]+"\" \""+self.conf335[3]+"\"\n")
        fp.write(self.conf336[0]+" \""+self.conf336[1]+"\" \""+self.conf336[2]+"\" \""+self.conf336[3]+"\"\n")
        fp.write(self.conf337[0]+" \""+self.conf337[1]+"\" \""+self.conf337[2]+"\" \""+self.conf337[3]+"\"\n")
        fp.write(self.conf338[0]+" \""+self.conf338[1]+"\" \""+self.conf338[2]+"\" \""+self.conf338[3]+"\"\n")
        fp.write(self.conf339[0]+" \""+self.conf339[1]+"\" \""+self.conf339[2]+"\" \""+self.conf339[3]+"\"\n")
        fp.write(self.conf340[0]+" \""+self.conf340[1]+"\" \""+self.conf340[2]+"\" \""+self.conf340[3]+"\"\n")
        fp.write(self.conf341[0]+" \""+self.conf341[1]+"\" \""+self.conf341[2]+"\" \""+self.conf341[3]+"\"\n")
        fp.write(self.conf342[0]+" \""+self.conf342[1]+"\" \""+self.conf342[2]+"\" \""+self.conf342[3]+"\"\n")
        fp.write(self.conf343[0]+" \""+self.conf343[1]+"\" \""+self.conf343[2]+"\" \""+self.conf343[3]+"\"\n")
        fp.write(self.conf344[0]+" \""+self.conf344[1]+"\" \""+self.conf344[2]+"\" \""+self.conf344[3]+"\"\n")
        fp.write(self.conf345[0]+" \""+self.conf345[1]+"\" \""+self.conf345[2]+"\" \""+self.conf345[3]+"\"\n")
        fp.write(self.conf346[0]+" \""+self.conf346[1]+"\" \""+self.conf346[2]+"\" \""+self.conf346[3]+"\"\n")
        fp.write(self.conf347[0]+" \""+self.conf347[1]+"\" \""+self.conf347[2]+"\" \""+self.conf347[3]+"\"\n")
        fp.write(self.conf348[0]+" \""+self.conf348[1]+"\" \""+self.conf348[2]+"\" \""+self.conf348[3]+"\"\n")
        fp.write(self.conf349[0]+" \""+self.conf349[1]+"\" \""+self.conf349[2]+"\" \""+self.conf349[3]+"\"\n")
        fp.write(self.conf350[0]+" \""+self.conf350[1]+"\" \""+self.conf350[2]+"\" \""+self.conf350[3]+"\"\n")
        fp.write(self.conf351[0]+" \""+self.conf351[1]+"\" \""+self.conf351[2]+"\" \""+self.conf351[3]+"\"\n")
        fp.write(self.conf352[0]+" \""+self.conf352[1]+"\" \""+self.conf352[2]+"\" \""+self.conf352[3]+"\"\n")
        fp.write(self.conf353[0]+" \""+self.conf353[1]+"\" \""+self.conf353[2]+"\" \""+self.conf353[3]+"\"\n")
        fp.write(self.conf354[0]+" \""+self.conf354[1]+"\" \""+self.conf354[2]+"\" \""+self.conf354[3]+"\"\n")
        fp.write(self.conf355[0]+" \""+self.conf355[1]+"\" \""+self.conf355[2]+"\" \""+self.conf355[3]+"\"\n")
        fp.write(self.conf356[0]+" \""+self.conf356[1]+"\" \""+self.conf356[2]+"\" \""+self.conf356[3]+"\"\n")
        fp.write(self.conf357[0]+" \""+self.conf357[1]+"\" \""+self.conf357[2]+"\" \""+self.conf357[3]+"\"\n")
        fp.write(self.conf358[0]+" \""+self.conf358[1]+"\" \""+self.conf358[2]+"\" \""+self.conf358[3]+"\"\n")
        fp.write(self.conf359[0]+" \""+self.conf359[1]+"\" \""+self.conf359[2]+"\" \""+self.conf359[3]+"\"\n")
        fp.write(self.conf360[0]+" \""+self.conf360[1]+"\" \""+self.conf360[2]+"\" \""+self.conf360[3]+"\"\n")
        fp.close()
        os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)
    #
    #   For game settings local which is also required
    def createFileLocal(self,file):
        if exists(file):
            os.chmod(file,stat.S_IWRITE )
        fp = open(file, 'w')
        fp.write(self.conf237[0]+" \""+self.conf237[1]+"\" \""+self.conf237[2]+"\" \""+self.conf237[3]+"\"\n")
        fp.write(self.conf223[0]+" \""+self.conf223[1]+"\" \""+self.conf223[2]+"\" \""+self.conf223[3]+"\"\n")
        fp.write(self.conf235[0]+" \""+self.conf235[1]+"\" \""+self.conf235[2]+"\" \""+self.conf235[3]+"\"\n")
        fp.write(self.conf357[0]+" \""+self.conf357[1]+"\" \""+self.conf357[2]+"\" \""+self.conf357[3]+"\"\n")
        fp.write(self.conf245[0]+" \""+self.conf245[1]+"\" \""+self.conf245[2]+"\" \""+self.conf245[3]+"\"\n")
        fp.write(self.conf226[0]+" \""+self.conf226[1]+"\" \""+self.conf226[2]+"\" \""+self.conf226[3]+"\"\n")
        fp.write(self.conf236[0]+" \""+self.conf236[1]+"\" \""+self.conf236[2]+"\" \""+self.conf236[3]+"\"\n")
        fp.write(self.conf225[0]+" \""+self.conf225[1]+"\" \""+self.conf225[2]+"\" \""+self.conf225[3]+"\"\n")
        fp.write(self.conf358[0]+" \""+self.conf358[1]+"\" \""+self.conf358[2]+"\" \""+self.conf358[3]+"\"\n")
        fp.write(self.conf359[0]+" \""+self.conf359[1]+"\" \""+self.conf359[2]+"\" \""+self.conf359[3]+"\"\n")
        fp.write(self.conf360[0]+" \""+self.conf360[1]+"\" \""+self.conf360[2]+"\" \""+self.conf360[3]+"\"\n")
        fp.write(self.conf356[0]+" \""+self.conf356[1]+"\" \""+self.conf356[2]+"\" \""+self.conf356[3]+"\"\n")
        fp.write(self.conf264[0]+" \""+self.conf264[1]+"\" \""+self.conf264[2]+"\" \""+self.conf264[3]+"\"\n")
        fp.close()
        os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)