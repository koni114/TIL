"?C
BHostIDLE"IDLE1     ?@A     ?@a)2M4[??i)2M4[???Unknown
rHostDataset"Iterator::Root::ParallelMapV2(1     ?q@9     ?q@A     ?q@I     ?q@a\?1q??if??W	???Unknown
?HostDataset">Iterator::Root::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate(1     `a@9     `a@A     ?`@I     ?`@a?w??ۅ??i??i?Q???Unknown
wHostDataset""Iterator::Root::ParallelMapV2::Zip(1     ?g@9     ?g@A      I@I      I@a?,?T????iAr?;????Unknown
^HostGatherV2"GatherV2(1     ?@@9     ?@@A     ?@@I     ?@@a^j=Bq7??i?g????Unknown
tHostMatMul" gradient_tape/model/dense/MatMul(1      <@9      <@A      <@I      <@a??Z?H'??i??j??a???Unknown
`HostDivNoNan"
div_no_nan(1      8@9      8@A      8@I      8@a?????g}?ir??x?????Unknown
vHostMatMul""gradient_tape/model/dense_1/MatMul(1      8@9      8@A      8@I      8@a?????g}?ibg?MV????Unknown
l	HostIteratorGetNext"IteratorGetNext(1      7@9      7@A      7@I      7@a????@.|?i?H8ϲ???Unknown
?
HostBiasAddGrad"-gradient_tape/model/dense/BiasAdd/BiasAddGrad(1      7@9      7@A      7@I      7@a????@.|?in*?PH???Unknown
?HostResourceApplyGradientDescent"-SGD/SGD/update_2/ResourceApplyGradientDescent(1      6@9      6@A      6@I      6@aӍ???z?i?#?~?}???Unknown
~HostReadVariableOp""model/dense/BiasAdd/ReadVariableOp(1      6@9      6@A      6@I      6@aӍ???z?i?֬?????Unknown
?HostReadVariableOp"$model/dense_2/BiasAdd/ReadVariableOp(1      6@9      6@A      6@I      6@aӍ???z?i????????Unknown
HostReadVariableOp"#model/dense_1/MatMul/ReadVariableOp(1      4@9      4@A      4@I      4@a?#wC?x?i
>?a????Unknown
uHostFlushSummaryWriter"FlushSummaryWriter(1      3@9      3@A      3@I      3@a????Gw?i?},?\I???Unknown?
?HostBiasAddGrad"/gradient_tape/model/dense_1/BiasAdd/BiasAddGrad(1      2@9      2@A      2@I      2@a۹+??v?i\?uxu???Unknown
xHostMatMul"$gradient_tape/model/dense_1/MatMul_1(1      (@9      (@A      (@I      (@a?????gm?iT??_?????Unknown
jHost_FusedMatMul"model/dense/Relu(1      &@9      &@A      &@I      &@aӍ???j?iⶔ?ԭ???Unknown
cHostDataset"Iterator::Root(1      r@9      r@A       @I       @a?OC_??c?i2???o????Unknown
iHostWriteSummary"WriteSummary(1      @9      @A      @I      @a??Z?H'a?iU?ۖ????Unknown?
gHostStridedSlice"strided_slice(1      @9      @A      @I      @a??Z?H'a?i???$?????Unknown
}HostMaximum"(gradient_tape/mean_squared_error/Maximum(1      @9      @A      @I      @a?????g]?iz"?r????Unknown
oHost_FusedMatMul"model/dense_2/BiasAdd(1      @9      @A      @I      @a?????g]?i??)&???Unknown
`HostGatherV2"
GatherV2_1(1      @9      @A      @I      @a?#wC?X?i??f???Unknown
?HostDataset"NIterator::Root::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice(1      @9      @A      @I      @a?#wC?X?i??R????Unknown
?HostResourceApplyGradientDescent"-SGD/SGD/update_3/ResourceApplyGradientDescent(1      @9      @A      @I      @a?#wC?X?i,3\??%???Unknown
?HostResourceApplyGradientDescent"-SGD/SGD/update_4/ResourceApplyGradientDescent(1      @9      @A      @I      @a?#wC?X?i>??(2???Unknown
?HostDynamicStitch".gradient_tape/mean_squared_error/DynamicStitch(1      @9      @A      @I      @a?#wC?X?iPG?7i>???Unknown
vHostMatMul""gradient_tape/model/dense_2/MatMul(1      @9      @A      @I      @a?#wC?X?ibю٩J???Unknown
?HostDataset"@Iterator::Root::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor(1      @9       @A      @I       @a?OC_??S?i
s?'wT???Unknown
xHostMatMul"$gradient_tape/model/dense_2/MatMul_1(1      @9      @A      @I      @a?OC_??S?i??uD^???Unknown
l Host_FusedMatMul"model/dense_1/Relu(1      @9      @A      @I      @a?OC_??S?iZ??h???Unknown
e!Host
LogicalAnd"
LogicalAnd(1      @9      @A      @I      @a?????gM?i?o??ko???Unknown?
?"HostResourceApplyGradientDescent"+SGD/SGD/update/ResourceApplyGradientDescent(1      @9      @A      @I      @a?????gM?i?(e??v???Unknown
?#HostResourceApplyGradientDescent"-SGD/SGD/update_1/ResourceApplyGradientDescent(1      @9      @A      @I      @a?????gM?i??~???Unknown
?$HostResourceApplyGradientDescent"-SGD/SGD/update_5/ResourceApplyGradientDescent(1      @9      @A      @I      @a?????gM?iR???y????Unknown
?%HostCast"2mean_squared_error/weighted_loss/num_elements/Cast(1      @9      @A      @I      @a?????gM?i?TP?ӌ???Unknown
n&HostConcatV2"model/concatenate/concat(1      @9      @A      @I      @a?????gM?i???-????Unknown
}'HostReadVariableOp"!model/dense/MatMul/ReadVariableOp(1      @9      @A      @I      @a?????gM?iǗ??????Unknown
t(HostAssignAddVariableOp"AssignAddVariableOp(1       @9       @A       @I       @a?OC_??C?i???En????Unknown
v)HostAssignAddVariableOp"AssignAddVariableOp_2(1       @9       @A       @I       @a?OC_??C?i?h??T????Unknown
?*HostDataset".Iterator::Root::ParallelMapV2::Zip[0]::FlatMap(1     ?a@9     ?a@A       @I       @a?OC_??C?i?9ߓ;????Unknown
s+HostReadVariableOp"SGD/Cast/ReadVariableOp(1       @9       @A       @I       @a?OC_??C?i\
?:"????Unknown
u,HostReadVariableOp"SGD/Cast_1/ReadVariableOp(1       @9       @A       @I       @a?OC_??C?i0??????Unknown
?-HostBroadcastTo",gradient_tape/mean_squared_error/BroadcastTo(1       @9       @A       @I       @a?OC_??C?i?&??????Unknown
w.HostCast"%gradient_tape/mean_squared_error/Cast(1       @9       @A       @I       @a?OC_??C?i?|>0ֽ???Unknown
u/HostSub"$gradient_tape/mean_squared_error/sub(1       @9       @A       @I       @a?OC_??C?i?MV׼????Unknown
?0HostTile"5gradient_tape/mean_squared_error/weighted_loss/Tile_1(1       @9       @A       @I       @a?OC_??C?i?n~?????Unknown
z1HostSlice"'gradient_tape/model/concatenate/Slice_1(1       @9       @A       @I       @a?OC_??C?iT??%?????Unknown
x2HostReluGrad""gradient_tape/model/dense/ReluGrad(1       @9       @A       @I       @a?OC_??C?i(???p????Unknown
?3HostBiasAddGrad"/gradient_tape/model/dense_2/BiasAdd/BiasAddGrad(1       @9       @A       @I       @a?OC_??C?i???sW????Unknown
i4HostMean"mean_squared_error/Mean(1       @9       @A       @I       @a?OC_??C?i?a?>????Unknown
?5HostSquaredDifference"$mean_squared_error/SquaredDifference(1       @9       @A       @I       @a?OC_??C?i?2??$????Unknown
u6HostSum"$mean_squared_error/weighted_loss/Sum(1       @9       @A       @I       @a?OC_??C?ix?h????Unknown
?7HostReadVariableOp"$model/dense_1/BiasAdd/ReadVariableOp(1       @9       @A       @I       @a?OC_??C?iL??????Unknown
8HostReadVariableOp"#model/dense_2/MatMul/ReadVariableOp(1       @9       @A       @I       @a?OC_??C?i ?,??????Unknown
v9HostAssignAddVariableOp"AssignAddVariableOp_1(1      ??9      ??A      ??I      ??a?OC_??3?i???
L????Unknown
V:HostCast"Cast(1      ??9      ??A      ??I      ??a?OC_??3?i?uD^?????Unknown
a;HostIdentity"Identity(1      ??9      ??A      ??I      ??a?OC_??3?i^^б2????Unknown?
|<HostAssignAddVariableOp"SGD/SGD/AssignAddVariableOp(1      ??9      ??A      ??I      ??a?OC_??3?i?F\?????Unknown
u=HostReadVariableOp"div_no_nan/ReadVariableOp(1      ??9      ??A      ??I      ??a?OC_??3?i2/?X????Unknown
u>HostMul"$gradient_tape/mean_squared_error/Mul(1      ??9      ??A      ??I      ??a?OC_??3?i?t??????Unknown
u?HostSum"$gradient_tape/mean_squared_error/Sum(1      ??9      ??A      ??I      ??a?OC_??3?i     ???Unknown
}@HostRealDiv"(gradient_tape/mean_squared_error/truediv(1      ??9      ??A      ??I      ??a?OC_??3?i8?ũ9???Unknown
?AHostDivNoNan"?gradient_tape/mean_squared_error/weighted_loss/value/div_no_nan(1      ??9      ??A      ??I      ??a?OC_??3?im??Ss???Unknown
zBHostReluGrad"$gradient_tape/model/dense_1/ReluGrad(1      ??9      ??A      ??I      ??a?OC_??3?i??Q?????Unknown
|CHostDivNoNan"&mean_squared_error/weighted_loss/value(1      ??9      ??A      ??I      ??a?OC_??3?i???????Unknown
'DHostMul"Mul(i???????Unknown
JEHostReadVariableOp"div_no_nan/ReadVariableOp_1(i???????Unknown
RFHostFloorDiv")gradient_tape/mean_squared_error/floordiv(i???????Unknown
JGHostMul"&gradient_tape/mean_squared_error/mul_1(i???????Unknown*?B
rHostDataset"Iterator::Root::ParallelMapV2(1     ?q@9     ?q@A     ?q@I     ?q@a?? ?????i?? ??????Unknown
?HostDataset">Iterator::Root::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate(1     `a@9     `a@A     ?`@I     ?`@a?9?G#???iq-?]y6???Unknown
wHostDataset""Iterator::Root::ParallelMapV2::Zip(1     ?g@9     ?g@A      I@I      I@a?I.?9??i?5???^???Unknown
^HostGatherV2"GatherV2(1     ?@@9     ?@@A     ?@@I     ?@@aPr??ᠢ?iM??????Unknown
tHostMatMul" gradient_tape/model/dense/MatMul(1      <@9      <@A      <@I      <@a?Mg?????i{?`>Ʌ???Unknown
`HostDivNoNan"
div_no_nan(1      8@9      8@A      8@I      8@a???@???i"?g??^???Unknown
vHostMatMul""gradient_tape/model/dense_1/MatMul(1      8@9      8@A      8@I      8@a???@???i?4o"R7???Unknown
lHostIteratorGetNext"IteratorGetNext(1      7@9      7@A      7@I      7@a???S????i~?e???Unknown
?	HostBiasAddGrad"-gradient_tape/model/dense/BiasAdd/BiasAddGrad(1      7@9      7@A      7@I      7@a???S????i3????????Unknown
?
HostResourceApplyGradientDescent"-SGD/SGD/update_2/ResourceApplyGradientDescent(1      6@9      6@A      6@I      6@aj?,f?֘?i?Tٺ~????Unknown
~HostReadVariableOp""model/dense/BiasAdd/ReadVariableOp(1      6@9      6@A      6@I      6@aj?,f?֘?i??
?2d???Unknown
?HostReadVariableOp"$model/dense_2/BiasAdd/ReadVariableOp(1      6@9      6@A      6@I      6@aj?,f?֘?i|<??*???Unknown
HostReadVariableOp"#model/dense_1/MatMul/ReadVariableOp(1      4@9      4@A      4@I      4@a\n?v???i\????????Unknown
uHostFlushSummaryWriter"FlushSummaryWriter(1      3@9      3@A      3@I      3@a?=?ps??iJ?&????Unknown?
?HostBiasAddGrad"/gradient_tape/model/dense_1/BiasAdd/BiasAddGrad(1      2@9      2@A      2@I      2@a???jR??iG?p?-???Unknown
xHostMatMul"$gradient_tape/model/dense_1/MatMul_1(1      (@9      (@A      (@I      (@a???@???i?7?????Unknown
jHost_FusedMatMul"model/dense/Relu(1      &@9      &@A      &@I      &@aj?,f?ֈ?i?驲u????Unknown
cHostDataset"Iterator::Root(1      r@9      r@A       @I       @a6???^??i??.?E???Unknown
iHostWriteSummary"WriteSummary(1      @9      @A      @I      @a?Mg????i$??y?????Unknown?
gHostStridedSlice"strided_slice(1      @9      @A      @I      @a?Mg????i?N??)????Unknown
}HostMaximum"(gradient_tape/mean_squared_error/Maximum(1      @9      @A      @I      @a???@?{?ii$]?Z????Unknown
oHost_FusedMatMul"model/dense_2/BiasAdd(1      @9      @A      @I      @a???@?{?i????0???Unknown
`HostGatherV2"
GatherV2_1(1      @9      @A      @I      @a\n?v?v?i?????]???Unknown
?HostDataset"NIterator::Root::ParallelMapV2::Zip[0]::FlatMap[0]::Concatenate[0]::TensorSlice(1      @9      @A      @I      @a\n?v?v?i???݊???Unknown
?HostResourceApplyGradientDescent"-SGD/SGD/update_3/ResourceApplyGradientDescent(1      @9      @A      @I      @a\n?v?v?i;?#?????Unknown
?HostResourceApplyGradientDescent"-SGD/SGD/update_4/ResourceApplyGradientDescent(1      @9      @A      @I      @a\n?v?v?i?l:?/????Unknown
?HostDynamicStitch".gradient_tape/mean_squared_error/DynamicStitch(1      @9      @A      @I      @a\n?v?v?i?IQ?X???Unknown
vHostMatMul""gradient_tape/model/dense_2/MatMul(1      @9      @A      @I      @a\n?v?v?ic&h??????Unknown
?HostDataset"@Iterator::Root::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor(1      @9       @A      @I       @a6???^r?i)
K?c???Unknown
xHostMatMul"$gradient_tape/model/dense_2/MatMul_1(1      @9      @A      @I      @a6???^r?i???Ç???Unknown
lHost_FusedMatMul"model/dense_1/Relu(1      @9      @A      @I      @a6???^r?i??k??????Unknown
e Host
LogicalAnd"
LogicalAnd(1      @9      @A      @I      @a???@?k?i???T?????Unknown?
?!HostResourceApplyGradientDescent"+SGD/SGD/update/ResourceApplyGradientDescent(1      @9      @A      @I      @a???@?k?i_???????Unknown
?"HostResourceApplyGradientDescent"-SGD/SGD/update_1/ResourceApplyGradientDescent(1      @9      @A      @I      @a???@?k?i4?.q-????Unknown
?#HostResourceApplyGradientDescent"-SGD/SGD/update_5/ResourceApplyGradientDescent(1      @9      @A      @I      @a???@?k?i	}o?E???Unknown
?$HostCast"2mean_squared_error/weighted_loss/num_elements/Cast(1      @9      @A      @I      @a???@?k?i?g??^3???Unknown
n%HostConcatV2"model/concatenate/concat(1      @9      @A      @I      @a???@?k?i?R?wN???Unknown
}&HostReadVariableOp"!model/dense/MatMul/ReadVariableOp(1      @9      @A      @I      @a???@?k?i?=2??i???Unknown
t'HostAssignAddVariableOp"AssignAddVariableOp(1       @9       @A       @I       @a6???^b?ik/	?{???Unknown
v(HostAssignAddVariableOp"AssignAddVariableOp_2(1       @9       @A       @I       @a6???^b?iN!?g?????Unknown
?)HostDataset".Iterator::Root::ParallelMapV2::Zip[0]::FlatMap(1     ?a@9     ?a@A       @I       @a6???^b?i1???????Unknown
s*HostReadVariableOp"SGD/Cast/ReadVariableOp(1       @9       @A       @I       @a6???^b?i?%ѱ???Unknown
u+HostReadVariableOp"SGD/Cast_1/ReadVariableOp(1       @9       @A       @I       @a6???^b?i??_??????Unknown
?,HostBroadcastTo",gradient_tape/mean_squared_error/BroadcastTo(1       @9       @A       @I       @a6???^b?i??5??????Unknown
w-HostCast"%gradient_tape/mean_squared_error/Cast(1       @9       @A       @I       @a6???^b?i??B????Unknown
u.HostSub"$gradient_tape/mean_squared_error/sub(1       @9       @A       @I       @a6???^b?i????????Unknown
?/HostTile"5gradient_tape/mean_squared_error/weighted_loss/Tile_1(1       @9       @A       @I       @a6???^b?i????"???Unknown
z0HostSlice"'gradient_tape/model/concatenate/Slice_1(1       @9       @A       @I       @a6???^b?if??^3???Unknown
x1HostReluGrad""gradient_tape/model/dense/ReluGrad(1       @9       @A       @I       @a6???^b?iI?c?C0???Unknown
?2HostBiasAddGrad"/gradient_tape/model/dense_2/BiasAdd/BiasAddGrad(1       @9       @A       @I       @a6???^b?i,?9TB???Unknown
i3HostMean"mean_squared_error/Mean(1       @9       @A       @I       @a6???^b?i?{dT???Unknown
?4HostSquaredDifference"$mean_squared_error/SquaredDifference(1       @9       @A       @I       @a6???^b?i?w??tf???Unknown
u5HostSum"$mean_squared_error/weighted_loss/Sum(1       @9       @A       @I       @a6???^b?i?i?8?x???Unknown
?6HostReadVariableOp"$model/dense_1/BiasAdd/ReadVariableOp(1       @9       @A       @I       @a6???^b?i?[???????Unknown
7HostReadVariableOp"#model/dense_2/MatMul/ReadVariableOp(1       @9       @A       @I       @a6???^b?i?Mg??????Unknown
v8HostAssignAddVariableOp"AssignAddVariableOp_1(1      ??9      ??A      ??I      ??a6???^R?i?F?%?????Unknown
V9HostCast"Cast(1      ??9      ??A      ??I      ??a6???^R?i?=U?????Unknown
a:HostIdentity"Identity(1      ??9      ??A      ??I      ??a6???^R?iq8???????Unknown?
|;HostAssignAddVariableOp"SGD/SGD/AssignAddVariableOp(1      ??9      ??A      ??I      ??a6???^R?ic1??????Unknown
u<HostReadVariableOp"div_no_nan/ReadVariableOp(1      ??9      ??A      ??I      ??a6???^R?iU*~??????Unknown
u=HostMul"$gradient_tape/mean_squared_error/Mul(1      ??9      ??A      ??I      ??a6???^R?iG#??????Unknown
u>HostSum"$gradient_tape/mean_squared_error/Sum(1      ??9      ??A      ??I      ??a6???^R?i9TB?????Unknown
}?HostRealDiv"(gradient_tape/mean_squared_error/truediv(1      ??9      ??A      ??I      ??a6???^R?i+?q?????Unknown
?@HostDivNoNan"?gradient_tape/mean_squared_error/weighted_loss/value/div_no_nan(1      ??9      ??A      ??I      ??a6???^R?i*??????Unknown
zAHostReluGrad"$gradient_tape/model/dense_1/ReluGrad(1      ??9      ??A      ??I      ??a6???^R?i???????Unknown
|BHostDivNoNan"&mean_squared_error/weighted_loss/value(1      ??9      ??A      ??I      ??a6???^R?i      ???Unknown
'CHostMul"Mul(i      ???Unknown
JDHostReadVariableOp"div_no_nan/ReadVariableOp_1(i      ???Unknown
REHostFloorDiv")gradient_tape/mean_squared_error/floordiv(i      ???Unknown
JFHostMul"&gradient_tape/mean_squared_error/mul_1(i      ???Unknown2CPU