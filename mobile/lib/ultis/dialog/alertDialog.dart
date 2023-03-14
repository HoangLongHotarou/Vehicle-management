// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/theme/app_color.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class alertDialog{
  static presentErrorDialog(BuildContext context, String? message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(builder: (context, setState) {
          return AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(20.0))),
              backgroundColor: Colors.white,
              content: Container(
                height: 180,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children:[
                    Icon(Icons.error_outline,size: 100,color: Colors.red,),
                    Text('${message}',
                        textAlign: TextAlign.center,
                        style: Theme.of(context)
                            .textTheme
                            .headline6!
                            .copyWith(color: AppColor.primaryColor))
                  ],
                ),
              ));
        });
      }
    ); 
  }
  static presentWarningDialog(BuildContext context, String? message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return StatefulBuilder(builder: (context, setState) {
          return AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(20.0))),
              backgroundColor: Colors.white,
              content: Container(
                height: 170,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children:[
                    Icon(Icons.warning_amber_outlined,size: 100,color: Colors.red,),
                    Text('${message}',textAlign: TextAlign.center,
                        style: Theme.of(context)
                            .textTheme
                            .headline6!
                            .copyWith(color: AppColor.primaryColor))
                  ],
                ),
              ));
        });
      }
    ); 
  }
  static presentSuccessDialog(BuildContext context, String? message) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return StatefulBuilder(builder: (context, setState) {
          return AlertDialog(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(20.0))),
              backgroundColor: Colors.white,
              content: Container(
                height: 170,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children:[
                    Icon(Icons.check_circle,size: 100,color: AppColor.primaryColor,),
                    Text('${message}',textAlign: TextAlign.center,
                        style: Theme.of(context)
                            .textTheme
                            .headline6!
                            .copyWith(color: AppColor.primaryColor))
                  ],
                ),
              ));
        });
      }
    ); 
  }
  static void dismisloading(context){
      Navigator.of(context).pop();
  }
}