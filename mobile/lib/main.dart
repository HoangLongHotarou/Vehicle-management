import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:license_plate_detect/feature/registervehicle/presention/register_vehicle_page.dart';
import 'package:license_plate_detect/feature/turninandout/presention/TurnInAndOutPage.dart';
import '/core/theme/app_theme.dart';
import 'feature/login/presention/LoginPage.dart';
import 'feature/home/presention/HomePage.dart';
import 'services/auth/auth.dart';

void main() async {
  await Hive.initFlutter();

  var token = await Hive.openBox('token');

  var user = await Hive.openBox('user');

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final Authenticate _auth = Authenticate();

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) { 
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        title: "License Plate Detect",
        theme: AppTheme.light,
        themeMode: ThemeMode.light,
        //home: LoginPage());
        home: FutureBuilder(
          future: _auth.checkLogin(),
          builder: ((context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return CircularProgressIndicator();
            } else if (snapshot.hasData) {
              if (snapshot.data == true) {
                return MyHomePage();
              } 
              return LoginPage();
            }
            return CircularProgressIndicator();
          }),
        ));
        //home: RegisterVehiclePage());
  }
}
