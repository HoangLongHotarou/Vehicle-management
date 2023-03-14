import 'dart:async';

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:license_plate_detect/core/models/checkAndDetail.dart';
import 'package:license_plate_detect/feature/login/presention/LoginPage.dart';
import 'package:license_plate_detect/services/auth/auth.dart';
import 'package:license_plate_detect/ultis/checkInternet/checkInternet.dart';
import 'package:license_plate_detect/ultis/toast/customtoast.dart';

import '../../../core/theme/app_color.dart';
import '../../../ultis/loading/customloading.dart';
import '../../register/presention/RegisterPage.dart';

class OTPPage extends StatefulWidget {
  OTPPage(
      {Key? key,
      required this.email,
      this.username,
      this.phonenumber,
      this.password})
      : super(key: key);

  String email;

  final String? username;
  final String? phonenumber;
  final String? password;

  @override
  State<OTPPage> createState() => _OTPPageState();
}

class _OTPPageState extends State<OTPPage> {
  TextEditingController otpController1 = new TextEditingController();
  TextEditingController otpController2 = new TextEditingController();
  TextEditingController otpController3 = new TextEditingController();
  TextEditingController otpController4 = new TextEditingController();

  var isDeviceConnected = false;
  bool isAlertSet = false;

  bool checkSpace() {
    bool check = true;
    if (otpController1.text == '' ||
        otpController2.text == '' ||
        otpController3.text == '' ||
        otpController4.text == '') {
      check = false;
    }
    return check;
  }

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
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Image(
              width: size.width,
              height: 200,
              fit: BoxFit.contain,
              image: const AssetImage("assets/img_otp.png"),
            ),
            Text(
              'Nhập OTP',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            Text(
              'Một mã code 4 số đã được gửi tới ${widget.email}',
              style: Theme.of(context)
                  .textTheme
                  .titleMedium
                  ?.copyWith(color: Colors.grey),
            ),
            const SizedBox(),
            SizedBox(
              height: 96,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    height: 86,
                    width: 72,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      color: AppColor.primarySwatch[50]?.withOpacity(0.5),
                    ),
                    padding: const EdgeInsets.all(8),
                    alignment: Alignment.center,
                    child: TextFormField(
                      controller: otpController1,
                      keyboardType: TextInputType.number,
                      style: Theme.of(context).textTheme.headlineMedium,
                      decoration: const InputDecoration(
                          contentPadding: EdgeInsets.all(0),
                          border: InputBorder.none),
                      textAlign: TextAlign.center,
                      inputFormatters: [
                        LengthLimitingTextInputFormatter(1),
                        FilteringTextInputFormatter.digitsOnly,
                      ],
                      onChanged: (value) {
                        if (value.isEmpty) {
                          return;
                        }
                        FocusScope.of(context).nextFocus();
                      },
                    ),
                  ),
                  Container(
                    height: 86,
                    width: 72,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      color: AppColor.primarySwatch[50]?.withOpacity(0.5),
                    ),
                    padding: const EdgeInsets.all(8),
                    alignment: Alignment.center,
                    child: TextFormField(
                      controller: otpController2,
                      keyboardType: TextInputType.number,
                      style: Theme.of(context).textTheme.headlineMedium,
                      decoration: const InputDecoration(
                          contentPadding: EdgeInsets.all(0),
                          border: InputBorder.none),
                      textAlign: TextAlign.center,
                      inputFormatters: [
                        LengthLimitingTextInputFormatter(1),
                        FilteringTextInputFormatter.digitsOnly,
                      ],
                      onChanged: (value) {
                        if (value.isEmpty) {
                          FocusScope.of(context).previousFocus();
                          return;
                        }
                        FocusScope.of(context).nextFocus();
                      },
                    ),
                  ),
                  Container(
                    height: 86,
                    width: 72,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      color: AppColor.primarySwatch[50]?.withOpacity(0.5),
                    ),
                    padding: const EdgeInsets.all(8),
                    alignment: Alignment.center,
                    child: TextFormField(
                      controller: otpController3,
                      keyboardType: TextInputType.number,
                      style: Theme.of(context).textTheme.headlineMedium,
                      decoration: const InputDecoration(
                          contentPadding: EdgeInsets.all(0),
                          border: InputBorder.none),
                      textAlign: TextAlign.center,
                      inputFormatters: [
                        LengthLimitingTextInputFormatter(1),
                        FilteringTextInputFormatter.digitsOnly,
                      ],
                      onChanged: (value) {
                        if (value.isEmpty) {
                          FocusScope.of(context).previousFocus();
                          return;
                        }
                        FocusScope.of(context).nextFocus();
                      },
                    ),
                  ),
                  Container(
                    height: 86,
                    width: 72,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(16),
                      color: AppColor.primarySwatch[50]?.withOpacity(0.5),
                    ),
                    padding: const EdgeInsets.all(8),
                    alignment: Alignment.center,
                    child: TextFormField(
                      controller: otpController4,
                      keyboardType: TextInputType.number,
                      style: Theme.of(context).textTheme.headlineMedium,
                      decoration: const InputDecoration(
                          contentPadding: EdgeInsets.all(0),
                          border: InputBorder.none),
                      textAlign: TextAlign.center,
                      inputFormatters: [
                        LengthLimitingTextInputFormatter(1),
                        FilteringTextInputFormatter.digitsOnly,
                      ],
                      onChanged: (value) {
                        if (value.isEmpty) {
                          FocusScope.of(context).nextFocus();
                          return;
                        }
                      },
                    ),
                  ),
                ],
              ),
            ),
            RichText(
                text: TextSpan(children: [
              TextSpan(
                  text: "Không nhận được mã ? ",
                  style: Theme.of(context)
                      .textTheme
                      .titleMedium
                      ?.copyWith(color: Colors.grey)),
              TextSpan(
                  text: "Gửi lại mã!",
                  style: Theme.of(context)
                      .textTheme
                      .button
                      ?.copyWith(color: AppColor.primaryColor),
                  recognizer: TapGestureRecognizer()
                    ..onTap = () async {
                      bool checkConnection = await checkInternet
                          .getConnectivity(isDeviceConnected, isAlertSet);
                      if (!checkConnection) {
                        checkInternet.showDialogBox(
                            context, isDeviceConnected, isAlertSet);
                        setState(
                          () => isAlertSet = true,
                        );
                      }else{
                        CheckAndDetail reg = await Authenticate.register(
                        widget.email,
                        widget.username!,
                        widget.phonenumber!,
                        widget.password!);
                        if (reg.check == true) {
                          CustomToast.presentSuccessToast(context,'Đã gửi lại mã đến ${widget.email}');
                        }else{
                          CustomToast.presentErrorToast(context,'Có lỗi xảy ra! Vui lòng thử lại');
                        }
                      }
                    }),
            ])),
            SizedBox(
              width: size.width,
              height: 64,
              child: ElevatedButton(
                onPressed: () async {
                  bool checkConnection = await checkInternet.getConnectivity(
                      isDeviceConnected, isAlertSet);
                  if (!checkConnection) {
                    checkInternet.showDialogBox(
                        context, isDeviceConnected, isAlertSet);
                    setState(
                      () => isAlertSet = true,
                    );
                  } else if (!checkSpace()) {
                    CustomToast.presentWarningToast(
                        context, 'Không được để trống các ô!');
                  } else {
                    String otp = otpController1.text +
                        otpController2.text +
                        otpController3.text +
                        otpController4.text;
                    CheckAndDetail reg = await Authenticate.otp(widget.email, otp);
                    CustomLoading.loadingtext(context, 'Đang đăng ký tài khoản');
                    if (reg.check == true) {
                      Timer(const Duration(milliseconds: 500), () {
                        CustomLoading.dismisloading(context);
                        CustomToast.presentSuccessToast(
                            context, 'Tạo tài khoản thành công!');
                        Navigator.push(context,
                            MaterialPageRoute(builder: (context) {
                          return LoginPage();
                        }));
                      });
                    } else if (reg.check == false) {
                      CustomLoading.dismisloading(context);
                      CustomToast.presentErrorToast(context, reg.detail);
                    }
                  }

                  // Navigator.push(context,
                  //             MaterialPageRoute(builder: (context) {
                  //           return LoginPage();
                  //         }));
                },
                style: ButtonStyle(
                    shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                        RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)))),
                child: const Text('Xác nhận'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
