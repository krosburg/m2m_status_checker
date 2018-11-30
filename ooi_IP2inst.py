
# Write out the port lookup table
ip2inst_table = {'LJ01A-J05-IP1' : 'HPIESA101',
                 'LJ01A-J09-IP5' : 'HYDBBA102',
                 'LJ01A-J10-IP6' : 'ADCPTE101',
                 'LJ01A-J11-IP7' : 'OPTAAC103',
                 'LJ01A-J12-IP8' : 'CTDPSB101',
                 'LJ01B-J05-IP1' : 'OBSBBA101',
                 'LJ01B-J06-IP2' : 'OBSSOA103',
                 'LJ01B-J07-IP3' : 'OBSSOA102',
                 'LJ01B-J08-IP4' : 'OBSSPA101',
                 'LJ01B-J09-IP5' : 'PRESTB102',
                 'LJ01B-J12-IP8' : 'VEL3DB104',
                 'LJ01C-J05-IP1' : 'ADCPSI103',
                 'LJ01C-J06-IP2' : 'CTDBPO108',
                 'LJ01C-J07-IP3' : 'VEL3DC107',
                 'LJ01C-J08-IP4' : 'OPTAAC104',
                 'LJ01C-J09-IP5' : 'PC02WB104',
                 'LJ01C-J10-IP6' : 'PHSEND107',
                 'LJ01C-J11-IP7' : 'HYDBBA105',
                 'LJ01D-J05-IP1' : 'ADCPTB104',
                 'LJ01D-J06-IP2' : 'CTDBPN106',
                 'LJ01D-J07-IP3' : 'VEL3DC108',
                 'LJ01D-J08-IP4' : 'OPTAAD106',
                 'LJ01D-J09-IP5' : 'PCO2WB103',
                 'LJ01D-J10-IP6' : 'PHSEND103',
                 'LJ01D-J11-IP7' : 'HYDBBA106',
                 'LJ03A-J05-IP1' : 'HPIESA301',
                 'LJ03A-J08-IP4' : 'expansion',
                 'LJ03A-J09-IP5' : 'HYDBBA302',
                 'LJ03A-J10-IP6' : 'ADCPTE301',
                 'LJ03A-J11-IP7' : 'OPTAAC303',
                 'LJ03A-J12-IP8' : 'CTDPFB301',
                 'LV01A-J02-EP1' : 'EXP-SP01A',
                 'LV01A-J03-EP2' : 'EXP-DP01A',
                 'LV01A-J05-IP1' : 'EXP-LJ01A',
                 'LV01B-J02-EP1' : 'EXP-MJ01B',
                 'LV01B-J05-IP1' : 'EXP-LJ01B',
                 'LV01C-J02-EP1' : 'EXP-SP01B',
                 'LV01C-J03-EP2' : 'EXP-DP01B',
                 'LV01C-J05-IP1' : 'EXP-LJ01C',
                 'LV01C-J06-IP2' : 'CAMDSB106',
                 'LV03A-J02-EP1' : 'EXP-SP03A',
                 'LV03A-J03-EP2' : 'EXP-DP03A',
                 'LV03A-J05-IP1' : 'EPX-LJ03A',
                 'MJ01A-J05-IP1' : 'OBSBKA101',
                 'MJ01A-J06-IP2' : 'PRESTA101',
                 'MJ01A-J12-IP8' : 'VEL3DB101',
                 'MJ01A-J05-IP1' : 'CAMDSB103',
                 'MJ01A-J06-IP2' : 'MASSPA101',
                 'MJ01A-J10-IP6' : 'QNTSRA101',
                 'MJ01A-J11-IP7' : 'CTDPFA110',
                 'MJ01A-J12-IP8' : 'ADCPSK101',
                 'MJ01C-J05-IP1' : 'EXP-LJ01D',
                 'MJ01C-J07-IP3' : 'ZPLSCB101',
                 'MJ01C-J09-IP4' : 'CAMDSB107',
                 'MJ03A-J05-IP1' : 'OBSBKA301',
                 'MJ03A-J06-IP2' : 'PRESTA301',
                 'MJ03A-J12-IP8' : 'VEL3DB301',
                 'MJ03B-J12-EP2' : 'COVISA301',
                 'MJ03B-J05-IP1' : 'OBSSPA302',
                 'MJ03B-J06-IP2' : 'OBSSPA301',
                 'MJ03B-J07-IP3' : 'TMPSFA301',
                 'MJ03B-J09-IP5' : 'BOTPTA304',
                 'MJ03B-J10-IP6' : 'CTDPFB304',
                 'MJ03B-J11-IP7' : 'HTVEHA301',
                 'MJ03C-J05-IP1' : 'CAMDSB303',
                 'MJ03C-J06-IP2' : 'MASSPA301',
                 'MJ03C-J07-IP3' : 'RASFLA301',
                 'MJ03C-J10-IP6' : 'TRHPHA301',
                 'MJ03D-J05-IP1' : 'OBSSPA305',
                 'MJ03D-J06-IP2' : 'BOTPTA303',
                 'MJ03D-J12-IP8' : 'VEL3DB304',
                 'MJ03E-J05-IP1' : 'OBSSPA303',
                 'MJ03E-J06-IP2' : 'BOTPTA302',
                 'MJ03E-J08-IP4' : 'OBSSPA304',
                 'MJ03E-J09-IP5' : 'OBSBBA302',
                 'MJ03F-J05-IP1' : 'BOTPTA301',
                 'MJ03F-J06-IP2' : 'OBSBKA101',
                 'MJ03F-J08-IP4' : 'SCTAA301',
                 'MJ03F-J09-IP5' : 'SCPRAA301',
                 'PC01A-J02-EP1' : 'EXP-SC01A',
                 'PC01A-J04A-IP1' : 'CTDPFA103',
                 'PC01A-J04B-IP2' : 'PHSENB102',
                 'PC01A-J04C-IP3' : 'FLORDD103',
                 'PC01A-J08-IP8' : 'HYDBBA103',
                 'PC01A-J05-IP9' : 'ADCPTD102',
                 'PC01A-J06-IP10' : 'VADCPA101',
                 'PC01A-J06-IP11' : 'VADCP(5TH)',
                 'PC01A-J07-IP12' : 'CAMDSC102',
                 'PC01B-J02-EP1' : 'EXP-SC01B',
                 'PC01B-J04A-IP1' : 'CTDPFA109',
                 'PC01B-J04B-IP2' : 'PHSENB106',
                 'PC01B-J04C-IP3' : 'PC02WA105',
                 'PC01B-J05-IP8' : 'ZPLSCB102',
                 'SF01A-J02A-IP1' : 'CTDPFA102',
                 'SF01A-J02D-IP3' : 'PHSENA101',
                 'SF01A-J03A-IP7' : 'FLORTD101',
                 'SF01A-J03B-IP8' : 'OPTAAD101',
                 'SF01A-J03C-IP9' : 'PARADA101',
                 'SF01A-J03B-IP10' : 'SPKIRA101',
                 'SF01A-J04A-IP12' : 'NUTNRA101',
                 'SF01A-J04B-IP13' : 'VELPTD102',
                 'SF01A-J04F-IP15' : 'PCO2WA101',
                 'SF01B-J02A-IP1' : 'CTDPFA107',
                 'SF01B-J03B-IP8' : 'OPTAAD105',
                 'SF01B-J03C-IP9' : 'PARADA102',
                 'SF01B-J04A-IP12' : 'NUTNRA102',
                 'SF01B-J04B-IP13' : 'VELPTD106',
                 'SF01B-J04F-IP15' : 'PCO2WA102',
                 'SF01B-J03B-IP10' : 'SPKIRA102'}


# Define the lookup function
def IP2inst(node, ipnum):
    key = node + '-' + ipnum
    return ip2inst_table[key]


print(IP2inst('PC01A','J02-EP1'))
