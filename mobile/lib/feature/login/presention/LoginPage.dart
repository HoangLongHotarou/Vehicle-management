// ignore_for_file: prefer_const_constructors, unrelated_type_equality_checks

import 'dart:async';

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/component/app_text_field.dart';
import 'package:license_plate_detect/core/models/Token.dart';
import 'package:license_plate_detect/core/theme/app_color.dart';
import 'package:license_plate_detect/feature/forgotpasssword/presention/ForgotPassword.dart';
import 'package:license_plate_detect/feature/register/presention/RegisterPage.dart';
import 'package:license_plate_detect/feature/home/presention/HomePage.dart';
import 'package:license_plate_detect/services/auth/auth.dart';
import 'package:license_plate_detect/services/localstorage/localStorage.dart';
import 'package:license_plate_detect/ultis/checkInternet/checkInternet.dart';
import 'package:license_plate_detect/ultis/loading/customloading.dart';
import 'package:license_plate_detect/ultis/toast/customtoast.dart';


class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController usernameController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  bool loading = true;
  Token token = new Token();

  bool showPassword = true;

  var isDeviceConnected = false;
  bool isAlertSet = false;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    Token token = LocalStorage.getToken();
    print(token.accessToken);
    print(token.tokenType);
    print('login');
  }

  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Scaffold(
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
              image: const AssetImage("assets/Lead_image.png"),
            ),
            Text(
              'Đăng nhập',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                AppTextFields(
                  controller: usernameController,
                  prefix: Icon(Icons.alternate_email_rounded),
                  hint: "Username",
                  textInputAction: TextInputAction.done,
                ),
                SizedBox(
                  height: 24,
                ),
                AppTextFields(
                  controller: passwordController,
                  obscureText: showPassword,
                  prefix: Icon(Icons.lock_outline_rounded),
                  suffix: IconButton(
                      onPressed: () {
                        setState(() {
                          showPassword = !showPassword;
                        });
                      },
                      icon: Icon(showPassword
                          ? Icons.visibility_outlined
                          : Icons.visibility_off_outlined)),
                  hint: "Mật khẩu",
                  textInputAction: TextInputAction.done,
                ),
              ],
            ),
            Align(
              alignment: Alignment.centerRight,
              child: TextButton(
                onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) {
                    return ForgotPasswordPage();
                  }));
                },
                child: Text('Quên mật khẩu?'),
              ),
            ),
            SizedBox(
              width: size.width,
              height: 64,
              child: ElevatedButton(
                onPressed: () async {
                  bool checkConnection = await checkInternet.getConnectivity(isDeviceConnected, isAlertSet);
                  if (!checkConnection) {
                    checkInternet.showDialogBox(context,isDeviceConnected,isAlertSet);
                    setState(
                      () => isAlertSet = true,
                    );
                  } else {
                    if (usernameController.text == '' || passwordController.text == '') {
                      //alertDialog.presentWarningDialog(context, 'Không được để trống\nusername hoặc mật khẩu!');
                      CustomToast.presentWarningToast(context,'Không được để trống\nusername hoặc mật khẩu!');
                    } else {
                      CustomLoading.loadingtext(context, 'Đang đăng nhập');
                      bool check = await Authenticate.login(usernameController.text, passwordController.text);
                      if (check == true) {
                        Timer(const Duration(milliseconds: 500), () {
                          CustomLoading.dismisloading(context);
                          Navigator.push(context,
                              MaterialPageRoute(builder: (context) {
                            return MyHomePage();
                          }));
                        });
                      } else if (check == false) {
                        CustomLoading.dismisloading(context);
                        CustomToast.presentErrorToast(context,
                            'Tài khoản hoặc mật khẩu\nkhông chính xác!');
                      }
                    }
                  }
                },
                style: ButtonStyle(
                    shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                        RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)))),
                child: const Text('Đăng nhập'),
              ),
            ),
            Align(
                alignment: Alignment.center,
                child: RichText(
                    text: TextSpan(children: [
                  TextSpan(
                      text: "Chưa có tài khoản ?",
                      style: Theme.of(context).textTheme.button),
                  TextSpan(
                      text: " Đăng ký ở đây!",
                      style: Theme.of(context)
                          .textTheme
                          .button
                          ?.copyWith(color: AppColor.primaryColor),
                      recognizer: TapGestureRecognizer()
                        ..onTap = () {
                          Navigator.push(context,
                              MaterialPageRoute(builder: (context) {
                            return RegisterPage();
                          }));
                        }),
                ])))
          ],
        ),
      ),
    );
  }
}
