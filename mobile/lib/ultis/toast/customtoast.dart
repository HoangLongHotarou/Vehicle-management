import 'package:awesome_snackbar_content/awesome_snackbar_content.dart';
import 'package:flutter/material.dart';

class CustomToast {
  static presentErrorToast(BuildContext context, String? message) {
    var snackBar = SnackBar(
      elevation: 0,
      behavior: SnackBarBehavior.floating,
      backgroundColor: Colors.transparent,
      duration: Duration(seconds: 2),
      content: AwesomeSnackbarContent(
        title: 'Lỗi!',
        message: '${message}',
        contentType: ContentType.failure,
      ),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
  static presentWarningToast(BuildContext context, String? message) {
    var snackBar = SnackBar(
      elevation: 0,
      behavior: SnackBarBehavior.floating,
      backgroundColor: Colors.transparent,
      duration: Duration(seconds: 2),
      content: AwesomeSnackbarContent(
        title: 'Chú ý!',
        message: '${message}',
        contentType: ContentType.warning,
      ),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
  static presentSuccessToast(BuildContext context, String? message) {
    var snackBar = SnackBar(
      elevation: 0,
      behavior: SnackBarBehavior.floating,
      backgroundColor: Colors.transparent,
      duration: Duration(seconds: 2),
      content: AwesomeSnackbarContent(
        title: 'Chúc mừng!',
        message: '${message}',
        contentType: ContentType.success,
      ),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
}
