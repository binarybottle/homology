i have run the adhd and part1 datasets through nipype (nipy.org/nipype) 
and rapidart artifact detection (within nipype) and found there to be 
very little motion. there were 14 subjects altogether that have motion 
exceeding 1mm at the center of at least one of the faces of the brains' 
bounding boxes for at least one of the volumes. there were only 5 subjects 
with more than two volumes with motion artifacts (corrected by mcflirt):

  ./adhd/sub20676:     Number of Motion Outliers: 9
  ./adhd/sub22608:     Number of Motion Outliers: 5
  ./controls/sub31671: Number of Motion Outliers: 15
  ./controls/sub38088: Number of Motion Outliers: 28
  ./controls/sub02503: Number of Motion Outliers: 4

there were no more than 6 volumes in any subject with intensity outliers
(>3 SD from mean).  i removed these volumes from the subjects.

in summary, i included all 25 adhd subjects and all 41 controls in the study.


grin -I stat*.txt -A 0 -B 0 -C 0 "Outliers"

./adhd/sub03951/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./adhd/sub08595/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./adhd/sub12486/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 1
./adhd/sub14299/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./adhd/sub14465/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./adhd/sub15758/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 1
./adhd/sub17109/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./adhd/sub20676/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 9
   18 : Number of Intensity Outliers: 0
./adhd/sub20691/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 2
./adhd/sub22349/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 2
   17 : Number of Intensity Outliers: 1
./adhd/sub22608/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 5
   17 : Number of Intensity Outliers: 1
./adhd/sub23844/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 6
./adhd/sub24528/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 2
./adhd/sub31554/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1
./adhd/sub48803/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 1
./adhd/sub53461/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./adhd/sub54828/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 1
   18 : Number of Intensity Outliers: 0
./adhd/sub56734/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 2
   17 : Number of Intensity Outliers: 0
./adhd/sub59796/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./adhd/sub63915/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./adhd/sub69779/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./adhd/sub73035/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./adhd/sub77203/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1
./adhd/sub77903/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./adhd/sub84371/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub01912/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 2
./controls/sub02503/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 4
   17 : Number of Intensity Outliers: 4
./controls/sub04856/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 2
./controls/sub05208/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 3
./controls/sub07578/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub09539/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1
./controls/sub10011/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1
./controls/sub10582/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub13384/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 1
   17 : Number of Intensity Outliers: 2
./controls/sub15213/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 1
   17 : Number of Intensity Outliers: 2
./controls/sub16607/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub17078/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub18638/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 4
./controls/sub19579/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub20732/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 1
   17 : Number of Intensity Outliers: 3
./controls/sub21212/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 2
./controls/sub26267/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 1
   18 : Number of Intensity Outliers: 1
./controls/sub27123/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub28795/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub28808/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub29216/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub29353/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub29935/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 1
   18 : Number of Intensity Outliers: 2
./controls/sub30247/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 2
./controls/sub30623/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub30860/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 2
./controls/sub31671/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 15
   19 : Number of Intensity Outliers: 4
./controls/sub33062/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1
./controls/sub33581/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub35262/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub37864/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 3
./controls/sub38088/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 28
   17 : Number of Intensity Outliers: 5
./controls/sub41546/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub44395/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub44515/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1
./controls/sub44979/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 2
./controls/sub45217/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 5
./controls/sub46856/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 2
./controls/sub47087/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 0
./controls/sub47633/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   18 : Number of Intensity Outliers: 0
./controls/sub48830/art/stats.rest_preprocessed.nii.txt:
    5 : Number of Motion Outliers: 0
   17 : Number of Intensity Outliers: 1

grin -I stat*.txt -A 0 -B 0 -C 0 "max: "

./adhd/sub03951/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00366347  0.00246895  0.00107318  0.135477    0.0532595   0.0854585 ] (motion: rot about x, y, z; trans along x, y, z)
   14 : max: 0.294626712187 (motion)
   19 : max: [ 2.76875211] (intensity)
./adhd/sub08595/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00794829  0.00256188  0.00198373  0.151497    0.0813362   0.0449661 ]
   15 : max: 0.630809814602
   20 : max: [ 2.65962978]
./adhd/sub12486/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  6.27977000e-03   5.99962000e-03   1.43094000e-03   1.48290000e-01
   15 : max: 0.542091102608
   20 : max: [ 2.08864929]
./adhd/sub14299/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00179229  0.00114818  0.00096958  0.0165122   0.101794    0.11945   ]
   14 : max: 0.200669391116
   19 : max: [ 2.57228903]
./adhd/sub14465/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00793528  0.00191517  0.00206453  0.0198584   0.134471    0.477199  ]
   15 : max: 0.267845868578
   20 : max: [ 2.51512976]
./adhd/sub15758/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00547392  0.00108118  0.00287846  0.17479     0.257608    0.210721  ]
   15 : max: 0.284342346186
   20 : max: [ 2.71194066]
./adhd/sub17109/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00292869  0.00049098  0.00113319  0.0609509   0.125263    0.122514  ]
   15 : max: 0.375937272175
   20 : max: [ 2.76731235]
./adhd/sub20676/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.0108347   0.00296056  0.00391028  0.131572    0.139775    0.348608  ]
   15 : max: 1.72349689551
   20 : max: [ 2.73548456]
./adhd/sub20691/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00780605  0.00398078  0.0018666   0.281472    0.300596    0.553429  ]
   14 : max: 0.503114469541
   19 : max: [ 2.78618829]
./adhd/sub22349/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.0127274   0.00196592  0.00065809  0.0444923   0.231919    0.638164  ]
   14 : max: 2.4073865396
   19 : max: [ 1.30259546]
./adhd/sub22608/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.0126025   0.0114019   0.00075428  0.0622859   0.23239     0.737542  ]
   14 : max: 1.34376115474
   19 : max: [ 2.04167137]
./adhd/sub23844/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00086233  0.00182772  0.00138976  0.0433982   0.249751    0.386559  ]
   15 : max: 0.293574704919
   20 : max: [ 2.1234766]
./adhd/sub24528/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.0045846   0.0010299   0.00200399  0.0214901   0.122232    0.247986  ]
   15 : max: 0.644765511199
   20 : max: [ 2.14089891]
./adhd/sub31554/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00329084  0.00121524  0.00067214  0.0233535   0.0615701   0.227607  ]
   14 : max: 0.248263971857
   19 : max: [ 3.02398628]
./adhd/sub48803/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00162798  0.00121158  0.00081792  0.0390059   0.12395     0.18323   ]
   15 : max: 0.233167373544
   20 : max: [ 2.05233673]
./adhd/sub53461/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00579677  0.00217918  0.00125779  0.110663    0.147987    0.128764  ]
   14 : max: 0.201896124692
   19 : max: [ 2.92189389]
./adhd/sub54828/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  1.33743000e-02   1.46079000e-04   5.18965000e-03   4.13766000e-01
   15 : max: 1.13882031412
   20 : max: [ 2.27029252]
./adhd/sub56734/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.0353945   0.00255598  0.00228211  0.0685925   0.710723    0.425676  ]
   14 : max: 2.00697694275
   19 : max: [ 2.1436634]
./adhd/sub59796/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00336714  0.00123023  0.00065583  0.0505634   0.216555    0.296753  ]
   15 : max: 0.390415780049
   20 : max: [ 2.96352914]
./adhd/sub63915/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00404508  0.00438917  0.0010433   0.0520313   0.0635789   0.139123  ]
   14 : max: 0.405735942804
   19 : max: [ 2.51008229]
./adhd/sub69779/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00134443  0.00055954  0.00077481  0.0245941   0.105877    0.129901  ]
   15 : max: 0.303370575813
   20 : max: [ 2.89872938]
./adhd/sub73035/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00288419  0.00199141  0.00059604  0.023438    0.0859928   0.118352  ]
   14 : max: 0.397676708091
   19 : max: [ 2.39232237]
./adhd/sub77203/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00195991  0.0020824   0.00117369  0.0391462   0.0470799   0.143357  ]
   14 : max: 0.22013373021
   19 : max: [ 2.7012958]
./adhd/sub77903/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00402603  0.00165973  0.00168665  0.0159131   0.101319    0.119906  ]
   15 : max: 0.170638951503
   20 : max: [ 2.54882234]
./adhd/sub84371/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00814009  0.00099822  0.00239213  0.175507    0.328896    0.856399  ]
   15 : max: 0.595834948628
   20 : max: [ 2.70607655]
./controls/sub01912/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00178382  0.00089536  0.00050709  0.0273662   0.0965185   0.103859  ]
   15 : max: 0.178457325503
   20 : max: [ 2.30253943]
./controls/sub02503/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00638399  0.00311612  0.00205369  0.113805    0.268905    0.450686  ]
   14 : max: 1.6879688679
   19 : max: [ 1.32120796]
./controls/sub04856/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  2.92099000e-02   1.76783000e-03   9.27810000e-04   2.87156000e-02
   15 : max: 0.868475524454
   20 : max: [ 1.81336788]
./controls/sub05208/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00654342  0.00202976  0.00169014  0.049539    0.07392     0.277733  ]
   14 : max: 0.457545453693
   19 : max: [ 1.99452157]
./controls/sub07578/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00779559  0.00126425  0.001699    0.0255886   0.0464882   0.0767635 ]
   14 : max: 0.537518426244
   19 : max: [ 1.70681632]
./controls/sub09539/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00672175  0.00245834  0.0006484   0.0632515   0.158647    0.224428  ]
   14 : max: 0.138127435721
   19 : max: [ 3.22693489]
./controls/sub10011/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.0037418   0.00126877  0.00244765  0.0696554   0.137611    0.309275  ]
   14 : max: 0.30375548094
   19 : max: [ 3.15101853]
./controls/sub10582/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00147136  0.00117072  0.00211888  0.105629    0.068868    0.147873  ]
   15 : max: 0.265146689826
   20 : max: [ 2.39130406]
./controls/sub13384/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.0106042   0.00366084  0.00074759  0.0444033   0.264726    0.440367  ]
   14 : max: 1.10483918275
   19 : max: [ 3.18626426]
./controls/sub15213/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00478099  0.00607847  0.00099642  0.052989    0.085508    0.91087   ]
   14 : max: 1.10287056257
   19 : max: [ 2.55454169]
./controls/sub16607/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00383081  0.00158387  0.00123111  0.0223042   0.051482    0.117166  ]
   15 : max: 0.240412055526
   20 : max: [ 2.58764355]
./controls/sub17078/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00196571  0.00137281  0.00137643  0.0941984   0.00372888  0.165773  ]
   15 : max: 0.308877091847
   20 : max: [ 2.68743134]
./controls/sub18638/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00234799  0.00093162  0.00109948  0.0800958   0.0745338   0.100496  ]
   14 : max: 0.128126234697
   19 : max: [ 2.28033191]
./controls/sub19579/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00145301  0.00132525  0.00169533  0.0800687   0.152152    0.185546  ]
   15 : max: 0.307888125173
   20 : max: [ 2.23736671]
./controls/sub20732/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00981943  0.00131964  0.00104311  0.0492898   0.0871142   0.445115  ]
   14 : max: 1.2764942827
   19 : max: [ 1.78368986]
./controls/sub21212/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00188815  0.00042931  0.00112662  0.0824052   0.158368    0.169393  ]
   15 : max: 0.618013078595
   20 : max: [ 1.72266677]
./controls/sub26267/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  3.91603000e-03   3.75601000e-03   1.39754000e-03   4.40504000e-02
   15 : max: 1.12953185346
   20 : max: [ 2.32141083]
./controls/sub27123/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00258782  0.00317329  0.00331189  0.127333    0.148229    0.364449  ]
   14 : max: 0.385385816672
   19 : max: [ 2.50290425]
./controls/sub28795/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  2.93495000e-04   2.03411000e-03   7.60672000e-04   4.37902000e-02
   15 : max: 0.5325532757
   20 : max: [ 1.84284573]
./controls/sub28808/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00238926  0.00225     0.00099516  0.0226566   0.0510331   0.080462  ]
   14 : max: 0.145230723029
   19 : max: [ 2.84077854]
./controls/sub29216/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  1.82133000e-04   2.09812000e-04   2.62189000e-03   1.29666000e-01
   15 : max: 0.387349821683
   20 : max: [ 2.01823428]
./controls/sub29353/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00479036  0.00453434  0.00245386  0.400663    0.295728    0.384332  ]
   15 : max: 0.366807339162
   20 : max: [ 2.6601326]
./controls/sub29935/art/stats.rest_preprocessed.nii.txt:
    9 : max: [  4.52481000e-03   1.79646000e-03   3.91240000e-04   2.61853000e-02
   15 : max: 1.14444767047
   20 : max: [ 2.54183337]
./controls/sub30247/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00466458  0.00205739  0.00112591  0.0365061   0.135671    0.115466  ]
   15 : max: 0.338041481884
   20 : max: [ 2.36258967]
./controls/sub30623/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00859852  0.00199469  0.0018995   0.0539388   0.0467391   0.0861152 ]
   15 : max: 0.387663417572
   20 : max: [ 2.45008984]
./controls/sub30860/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00354993  0.00128817  0.00175603  0.0375624  -0.00231318 -0.00561325]
   15 : max: 0.481706213456
   20 : max: [ 1.77971664]
./controls/sub31671/art/stats.rest_preprocessed.nii.txt:
   11 : max: [ 0.0471507   0.0077946   0.00491951  0.251699    0.613178    1.94737   ]
   16 : max: 2.97321329899
   21 : max: [ 2.49122824]
./controls/sub33062/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00656623  0.00099305  0.0024233   0.153294    0.146177    0.162585  ]
   14 : max: 0.223159130392
   19 : max: [ 2.26687497]
./controls/sub33581/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00293547  0.00303509  0.00136231  0.0402843   0.0556255   0.0510711 ]
   14 : max: 0.198629045868
   19 : max: [ 2.6172361]
./controls/sub35262/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.0016469   0.00081501  0.00118182  0.024622    0.0696995   0.0774272 ]
   15 : max: 0.214670853991
   20 : max: [ 2.38561783]
./controls/sub37864/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00326472  0.0028872   0.0025022   0.117849    0.155225    0.220003  ]
   14 : max: 0.453343580467
   19 : max: [ 1.85848309]
./controls/sub38088/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.034301    0.00632504  0.00531385  0.160787    0.563412    1.62408   ]
   14 : max: 3.87383153405
   19 : max: [ 1.55689484]
./controls/sub41546/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00277715  0.0023987   0.00195781  0.0245329   0.0743452   0.22231   ]
   14 : max: 0.159806507464
   19 : max: [ 1.86887315]
./controls/sub44395/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00137298  0.00139632  0.00113949  0.0255816   0.0653375   0.174273  ]
   14 : max: 0.250118360614
   19 : max: [ 2.74300166]
./controls/sub44515/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.004799    0.00077819  0.00201775  0.0743621   0.147441    0.425962  ]
   14 : max: 0.482167833012
   19 : max: [ 3.19243022]
./controls/sub44979/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00432822  0.00219368  0.00171399  0.040507    0.0578626   0.180938  ]
   14 : max: 0.299491537668
   19 : max: [ 2.73373297]
./controls/sub45217/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.00125527  0.00181859  0.00088119  0.030004    0.10028     0.238375  ]
   15 : max: 0.462984838712
   20 : max: [ 1.96257102]
./controls/sub46856/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.0427889   0.0015558   0.00699183  0.10958     0.437659    0.0763068 ]
   14 : max: 0.844590698183
   19 : max: [ 2.19499051]
./controls/sub47087/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00514803  0.00081065  0.0026746   0.166522    0.0848805   0.0920509 ]
   14 : max: 0.14878786305
   19 : max: [ 2.37444009]
./controls/sub47633/art/stats.rest_preprocessed.nii.txt:
   10 : max: [ 0.0121527   0.00443835  0.00219374  0.055426    0.255855    0.639322  ]
   15 : max: 0.171095963848
   20 : max: [ 2.38275869]
./controls/sub48830/art/stats.rest_preprocessed.nii.txt:
    9 : max: [ 0.00248964  0.00135646  0.00075103  0.117121    0.0675007   0.0591569 ]
   14 : max: 0.326698824898
   19 : max: [ 3.92781246]
