Puppet::Type.newtype(:interfaces/interface) do
  @doc = Interface parameters.
  ensurable
  feature :activable, "The ability to activate/deactive configuration"

  newparam( :name, :namevar=>true ) do
    desc "An arbitrary name for the interface"
  end

  newproperty( :description ) do
    desc "A textual description of the interface"
  end

  newproperty( :type ) do
    desc "The type of the interface"
    newvalues( other, regular1822, hdh1822, ddnX25, rfc877x25, ethernetCsmacd, iso88023Csmacd, iso88024TokenBus, iso88025TokenRing, iso88026Man, starLan, proteon10Mbit, proteon80Mbit, hyperchannel, fddi, lapb, sdlc, ds1, e1, basicISDN, primaryISDN, propPointToPointSerial, ppp, softwareLoopback, eon, ethernet3Mbit, nsip, slip, ultra, ds3, sip, frameRelay, rs232, para, arcnet, arcnetPlus, atm, miox25, sonet, x25ple, iso88022llc, localTalk, smdsDxi, frameRelayService, v35, hssi, hippi, modem, aal5, sonetPath, sonetVT, smdsIcip, propVirtual, propMultiplexor, ieee80212, fibreChannel, hippiInterface, frameRelayInterconnect, aflane8023, aflane8025, cctEmul, fastEther, isdn, v11, v36, g703at64k, g703at2mb, qllc, fastEtherFX, channel, ieee80211, ibm370parChan, escon, dlsw, isdns, isdnu, lapd, ipSwitch, rsrb, atmLogical, ds0, ds0Bundle, bsc, async, cnr, iso88025Dtr, eplrs, arap, propCnls, hostPad, termPad, frameRelayMPI, x213, adsl, radsl, sdsl, vdsl, iso88025CRFPInt, myrinet, voiceEM, voiceFXO, voiceFXS, voiceEncap, voiceOverIp, atmDxi, atmFuni, atmIma, pppMultilinkBundle, ipOverCdlc, ipOverClaw, stackToStack, virtualIpAddress, mpc, ipOverAtm, iso88025Fiber, tdlc, gigabitEthernet, hdlc, lapf, v37, x25mlp, x25huntGroup, transpHdlc, interleave, fast, ip, docsCableMaclayer, docsCableDownstream, docsCableUpstream, a12MppSwitch, tunnel, coffee, ces, atmSubInterface, l2vlan, l3ipvlan, l3ipxvlan, digitalPowerline, mediaMailOverIp, dtm, dcn, ipForward, msdsl, ieee1394, if-gsn, dvbRccMacLayer, dvbRccDownstream, dvbRccUpstream, atmVirtual, mplsTunnel, srp, voiceOverAtm, voiceOverFrameRelay, idsl, compositeLink, ss7SigLink, propWirelessP2P, frForward, rfc1483, usb, ieee8023adLag, bgppolicyaccounting, frf16MfrBundle, h323Gatekeeper, h323Proxy, mpls, mfSigLink, hdsl2, shdsl, ds1FDL, pos, dvbAsiIn, dvbAsiOut, plc, nfas, tr008, gr303RDT, gr303IDT, isup, propDocsWirelessMaclayer, propDocsWirelessDownstream, propDocsWirelessUpstream, hiperlan2, propBWAp2Mp, sonetOverheadChannel, digitalWrapperOverheadChannel, aal2, radioMAC, atmRadio, imt, mvl, reachDSL, frDlciEndPt, atmVciEndPt, opticalChannel, opticalTransport, propAtm, voiceOverCable, infiniband, teLink, q2931, virtualTg, sipTg, sipSig, docsCableUpstreamChannel, econet, pon155, pon622, bridge, linegroup, voiceEMFGD, voiceFGDEANA, voiceDID, mpegTransport, sixToFour, gtp, pdnEtherLoop1, pdnEtherLoop2, opticalChannelGroup, homepna, gfp, ciscoISLvlan, actelisMetaLOOP, fcipLink, rpr, qam, lmp, cblVectaStar, docsCableMCmtsDownstream, adsl2, macSecControlledIF, macSecUncontrolledIF, aviciOpticalEther, atmbond, voiceFGDOS, mocaVersion1, ieee80216WMAN, adsl2plus, dvbRcsMacLayer, dvbTdm, dvbRcsTdma, x86Laps, wwanPP, wwanPP2, voiceEBS, ifPwType, ilan, pip, aluELP, gpon, vdsl2, capwapDot11Profile, capwapDot11Bss, capwapWtpVirtualRadio, bits, docsCableUpstreamRfPort, cableDownstreamRfPort, vmwareVirtualNic, ieee802154, otnOdu, otnOtu, ifVfiType, g9981, g9982, g9983, aluEpon, aluEponOnu, aluEponPhysicalUni, aluEponLogicalLink, aluGponOnu, aluGponPhysicalUni, vmwareNicTeam )
  end

  newproperty( :location ) do
    desc "The device-specific location of the interface of aparticular type"
  end

  newproperty( :enabled ) do
    desc "The desired state of the interface"
    defaultto( :true )
    newvalues( true, false )
  end

  newproperty( :mtu ) do
    desc "The size, in octets, of the largest packet that theinterface can send and receive"
    munge { |v| Integer( v ) }
  end

  newproperty( :link-up-down-trap-enable ) do
    desc "Indicates whether linkUp/linkDown SNMP notificationsshould be generated for this interface"
    defaultto( :enabled )
    newvalues( enabled, disabled )
  end

  newproperty( :speed ) do
    desc "An estimate of the interface's current bandwidth in bitsper second"
    munge { |v| Integer( v ) }
  end

end

