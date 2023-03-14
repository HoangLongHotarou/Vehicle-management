import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/models/checkAndDetail.dart';
import 'package:license_plate_detect/core/theme/app_data.dart';
import 'package:license_plate_detect/feature/home/presention/HomePage.dart';
import 'package:license_plate_detect/services/auth/auth.dart';

import '../../../core/component/app_text_field.dart';
import '../../../core/theme/app_color.dart';

import 'package:license_plate_detect/ultis/checkInternet/checkInternet.dart';

import '../../../ultis/loading/customloading.dart';
import '../../../ultis/toast/customtoast.dart';

class RegisterVehiclePage extends StatefulWidget {
  const RegisterVehiclePage({super.key});

  @override
  State<RegisterVehiclePage> createState() => _RegisterVehiclePageState();
}

class _RegisterVehiclePageState extends State<RegisterVehiclePage> {
  TextEditingController plateController = TextEditingController();

  List<Map> vehicletypes = [
    {'id': '1', 'name': 'xe máy', 'image': AppData.icMotobike},
    {'id': '2', 'name': 'xe hơi', 'image': AppData.icCar},
  ];

  String? _selected;

  String? vehicletype;

  var isDeviceConnected = false;
  bool isAlertSet = false;

  final formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Icon(
            Icons.arrow_back_ios_new_rounded,
            color: AppColor.black,
          ),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      extendBodyBehindAppBar: true,
      body: Padding(
        padding: EdgeInsets.only(
            top: MediaQuery.of(context).padding.top,
            bottom: MediaQuery.of(context).padding.bottom,
            left: 24,
            right: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Image(
              width: size.width,
              height: 200,
              fit: BoxFit.contain,
              image: const AssetImage("assets/img_register.png"),
            ),
            Text(
              'Đăng ký xe',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // AppTextFields(
                //   controller: plateController,
                //   prefix: Image.asset("assets/icons/ic_plate.png",width: 32,height: 32),
                //   hint: "Biển số xe",
                //   textInputAction: TextInputAction.done,
                // ),
                Form(
                  key: formKey,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Image.asset(
                        AppData.icPlate,
                        width: 32,
                      ),
                      SizedBox(
                        width: 24,
                      ),
                      Expanded(
                        child: TextFormField(
                          controller: plateController,
                          decoration:
                              InputDecoration(labelText: 'Nhập biển số xe'),
                          validator: (value) {
                            if (value!.isEmpty ||
                                !RegExp(r'[1-9]{1}[0-9]{1}[A-Z]{1,2}[1-9]{0,1}[-]{1}[0-9]{4,5}')
                                    .hasMatch(value)) {
                              return 'Vui lòng nhập đúng biển số';
                            } else {
                              return null;
                            }
                          },
                        ),
                      )
                    ],
                  ),
                ),
                const SizedBox(
                  height: 24,
                ),
                Container(
                  decoration: BoxDecoration(
                      border: Border.all(width: 1, color: Colors.grey),
                      borderRadius: BorderRadius.circular(18)),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                          child: DropdownButtonHideUnderline(
                        child: ButtonTheme(
                          alignedDropdown: true,
                          child: DropdownButton(
                            hint: Text('Chọn loại xe'),
                            value: _selected,
                            onChanged: (value) {
                              setState(() {
                                _selected = value.toString();
                                _selected == '1'
                                    ? vehicletype = "motorcycle"
                                    : vehicletype = "car";
                                print(vehicletype);
                              });
                            },
                            items: vehicletypes.map((Map map) {
                              return DropdownMenuItem(
                                value: map['id'].toString(),
                                child: Row(children: [
                                  Image.asset(map['image']),
                                  Container(
                                    margin: EdgeInsets.only(left: 18),
                                    child: Text(map['name']),
                                  )
                                ]),
                              );
                            }).toList(),
                          ),
                        ),
                      ))
                    ],
                  ),
                )
              ],
            ),
            SizedBox(
              width: size.width,
              height: 48,
              child: ElevatedButton(
                onPressed: () async {
                  bool checkConnection = await checkInternet.getConnectivity(
                      isDeviceConnected, isAlertSet);
                  if (!checkConnection) {
                    checkInternet.showDialogBox(
                        context, isDeviceConnected, isAlertSet);
                    setState(() {
                      isAlertSet = true;
                    });
                  } else {
                    if (formKey.currentState!.validate()) {
                      if (vehicletype == null) {
                        CustomToast.presentWarningToast(
                            context, 'Vui lòng chọn loại xe!');
                      } else {
                        CustomLoading.loadingtext(
                            context, 'Đang đăng ký tài khoản');
                        CheckAndDetail cks = await Authenticate.registerVehicle(
                            plateController.text, vehicletype!);
                        if (cks.check == true) {
                          CustomLoading.dismisloading(context);
                          CustomToast.presentSuccessToast(
                              context, 'Đăng ký xe thành công!');
                          Navigator.push(context,
                              MaterialPageRoute(builder: (context) {
                            return const MyHomePage();
                          }));
                        } else if (cks.check == false) {
                          CustomLoading.dismisloading(context);
                          CustomToast.presentErrorToast(
                              context, '${cks.detail}');
                        }
                      }
                    }
                  }
                },
                style: ButtonStyle(
                    shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                        RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)))),
                child: const Text(
                  'Đăng ký xe',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
