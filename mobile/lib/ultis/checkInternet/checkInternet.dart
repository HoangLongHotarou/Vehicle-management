import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:internet_connection_checker/internet_connection_checker.dart';

class checkInternet{
  static Future<bool> getConnectivity(bool isDeviceConnected,bool isAlertSet) async {
    bool check = true;
    isDeviceConnected = await InternetConnectionChecker().hasConnection;
    if (!isDeviceConnected && isAlertSet == false) {
      // showDialogBox();
      // setState(() {
      //   isAlertSet = true;
      // });
      check = false;
    }
    return check;
  }
  static showDialogBox(BuildContext context,bool isDeviceConnected,bool isAlertSet)=> showCupertinoDialog<String>(
      context: context,
      builder: (BuildContext context) => CupertinoAlertDialog(
            title: const Text('Không có kết nối mạng'),
            content: const Text('Vui lòng kiểm tra kết nối mạng của bạn'),
            actions: <Widget>[
              TextButton(
                  onPressed: () async {
                    Navigator.pop(context, 'Cancel');
                    isAlertSet = false;
                    isDeviceConnected =
                        await InternetConnectionChecker().hasConnection;
                    if (!isDeviceConnected && isAlertSet == false) {
                      showDialogBox(context,isDeviceConnected,isAlertSet);
                      isAlertSet = true;
                    }
                  },
                  child: const Text('OK'))
            ],
          ));
}